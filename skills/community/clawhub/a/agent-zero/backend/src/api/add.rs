//! Listing ingest endpoints — add and suggest new listings.
//!
//! Fetches and parses the given listing URL, saves the result to the DB,
//! downloads images, and returns the saved record.
//!
//! # Supported parsers
//!
//! | Source      | Status  | Notes                                      |
//! |-------------|---------|--------------------------------------------|  
//! | Redfin      | ✅ Works | Primary source; best structured data       |
//! | REW.ca      | ✅ Works | Good supplement; includes property tax     |
//! | Zillow      | ❌ Blocked | PerimeterX / CloudFront (403)            |
//! | Realtor.ca  | ❌ Blocked | Imperva Incapsula                        |
//!
//! # Blocked-host handling
//!
//! When the submitted URL is from a known-blocked host (Zillow, Realtor.ca),
//! a stub listing is saved containing only the URL so the user can fill in
//! details manually via the edit panel.
//!
//! Endpoints:
//! - `POST /api/listings`         — human-driven add (defaults to Interested)
//! - `POST /api/listings/agent-suggest` — AI-driven suggest (AgentPending, no profile; agent assigns)

use axum::{extract::State, http::StatusCode, Json};
use serde::Deserialize;

use crate::fetching::fetch::fetch_html;
use crate::fetching::html_snapshots::save_listing_html;
use crate::fetching::url::parse_listing_url;
use crate::models::property::{ListingStatus, Property, StoredProperty};
use crate::finance as property_finance;
use crate::store::{image_store, open_house_store, property_store, search_profile_store};
use crate::{images, parsers, AppState};

#[derive(Deserialize)]
pub struct AddRequest {
    /// The listing URL to add.
    pub url: String,
    /// Search profile to assign this listing to.
    pub search_profile_id: i64,
}

/// Body for POST /api/listings/agent-suggest — agent/skill workflow.
/// No search_profile_id: the agent assigns the profile during review.
#[derive(Deserialize)]
pub struct SuggestRequest {
    pub url: String,
}

/// POST /api/listings
///
/// Human-driven listing ingest endpoint. Saves the property with `Interested`
/// status and requires a valid `search_profile_id`.
pub(crate) async fn add_listing(
    State(state): State<AppState>,
    Json(body): Json<AddRequest>,
) -> Result<Json<Property>, (StatusCode, String)> {
    let property = add_listing_impl(state, body, ListingStatus::Interested).await?;
    Ok(Json(property))
}

/// POST /api/listings/agent-suggest
///
/// AI/skill-driven listing ingest endpoint. Saves the property with
/// `AgentPending` status and no search profile. After saving, spawns a
/// background task that calls the Claude API to triage the listing and assign
/// a search profile (or skip it).
pub(crate) async fn suggest_listing(
    State(state): State<AppState>,
    Json(body): Json<SuggestRequest>,
) -> Result<Json<Property>, (StatusCode, String)> {
    let add_body = AddRequest {
        url: body.url,
        search_profile_id: 0, // ignored by suggest path — overridden below
    };
    let property = add_listing_impl(state.clone(), add_body, ListingStatus::AgentPending).await?;

    // Spawn background agent review (assigns profile + moves to HumanReview or AgentSkip).
    let db = state.db.clone();
    let client = state.client.clone();
    let listing_id = property.id;
    let stored = crate::models::property::StoredProperty::from(property.clone());
    tokio::spawn(async move {
        crate::agent::review::run_agent_review(listing_id, stored, db, client).await;
    });

    Ok(Json(property))
}

async fn add_listing_impl(
    state: AppState,
    body: AddRequest,
    initial_status: ListingStatus,
) -> Result<Property, (StatusCode, String)> {
    // Validate search profile exists before doing any expensive work.
    // search_profile_id==0 is the sentinel used by suggest_listing (no profile yet).
    if body.search_profile_id != 0 {
        search_profile_store::get_by_id(&state.db, body.search_profile_id)
            .await
            .map_err(|e| match e {
                sqlx::Error::RowNotFound => (
                    StatusCode::BAD_REQUEST,
                    format!("search_profile_id {} does not exist", body.search_profile_id),
                ),
                _ => (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")),
            })?;
    }

    let trimmed_url = body.url.trim();
    let listing_url = parse_listing_url(trimmed_url).ok_or((
        StatusCode::BAD_REQUEST,
        format!("Invalid URL: {trimmed_url}"),
    ))?;
    let site = listing_url.site;
    let parsed_url = listing_url.url;

    // Check for duplicate source URLs before fetching.
    if let Ok(Some(existing)) = property_store::find_by_source_url(&state.db, parsed_url.as_str()).await {
        let body = serde_json::json!({
            "duplicate": true,
            "existing_id": existing.id,
            "existing_title": existing.title,
            "mls_number": existing.mls_number,
        });
        return Err((StatusCode::CONFLICT, body.to_string()));
    }

    // Fetch HTML.
    // `fetch_html` tries a direct HTTP request first.  For bot-protected
    // hosts (Zillow, Realtor.ca) it automatically falls back to Safari via
    // AppleScript.  If even that fails, we save an empty stub so the user
    // can fill in details manually.
    let source = match fetch_html(&state.client, &parsed_url).await {
        Ok(html) => parsers::SourceInput {
            url: parsed_url.to_string(),
            html,
        },
        Err(e) if is_blocked_host(site) => {
            tracing::info!(
                "add_listing: fetch failed for {} ({}), saving stub",
                parsed_url,
                e
            );
            parsers::SourceInput {
                url: parsed_url.to_string(),
                html: String::new(),
            }
        }
        Err(e) => {
            return Err((
                StatusCode::BAD_GATEWAY,
                format!("Failed to fetch {}: {}", parsed_url, e),
            ))
        }
    };

    let listing_opt = parsers::parse_multi(std::slice::from_ref(&source));

    let (mut property, image_urls, open_houses) = match listing_opt {
        Some(listing) => (listing.property, listing.image_urls, listing.open_houses),
        None => {
            // Parsing yielded nothing.  Only save a stub for known-blocked hosts;
            // for unrecognised URLs return 422.
            if !is_blocked_host(site) {
                return Err((
                    StatusCode::UNPROCESSABLE_ENTITY,
                    "No recognized listing format found in page".to_string(),
                ));
            }
            tracing::info!(
                "add_listing: all URLs are from blocked hosts, saving stub for {:?}",
                parsed_url.as_str(),
            );
            let mut stub = blank_stub();
            // Populate whichever URL fields we know about.
            match site {
                parsers::ListingSite::Zillow => stub.zillow_url = Some(parsed_url.to_string()),
                parsers::ListingSite::Realtor => stub.realtor_url = Some(parsed_url.to_string()),
                _ => {}
            }
            (stub, vec![], vec![])
        }
    };

    // Auto-calculate mortgage with defaults on first save.
    let down_pct = property.down_payment_pct.unwrap_or(0.20);
    let rate = property.mortgage_interest_rate.unwrap_or(0.04);
    let years = property.amortization_years.unwrap_or(25);
    property.down_payment_pct = Some(down_pct);
    property.mortgage_interest_rate = Some(rate);
    property.amortization_years = Some(years);
    let finance = property_finance::compute(
        property.price, property.offer_price, down_pct, rate, years,
        property.property_tax, property.hoa_monthly,
    );
    property.mortgage_monthly = finance.mortgage_monthly;
    property.monthly_total = finance.monthly_total;
    property.monthly_cost = finance.monthly_cost;

    // Check for duplicate MLS number before inserting.
    if let Some(ref mls) = property.mls_number {
        if let Ok(Some(existing)) = property_store::find_by_mls(&state.db, mls).await {
            let body = serde_json::json!({
                "duplicate": true,
                "existing_id": existing.id,
                "existing_title": existing.title,
                "mls_number": mls,
            });
            return Err((StatusCode::CONFLICT, body.to_string()));
        }
    }

    // Assign to search profile (skipped for suggest path where id==0).
    if body.search_profile_id != 0 {
        property.search_profile_id = Some(body.search_profile_id);
    }
    property.status = initial_status;

    let saved = property_store::add_listing(&state.db, &property).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("DB error: {}", e),
        )
    })?;

    // Save any parsed open house events (upsert — ignore duplicates).
    if !open_houses.is_empty() {
        if let Err(e) = open_house_store::upsert_open_houses(&state.db, saved.id, &open_houses).await {
            tracing::warn!("add_listing: failed to save open houses for id={}: {}", saved.id, e);
        }
    }

    // Register image URLs in images_cache, preserving parser ordering.
    tracing::info!(
        "add_listing: id={} registering {} image URL(s)",
        saved.id,
        image_urls.len()
    );

    // Save raw HTML snapshots for offline inspection / parser backfills.
    save_listing_html(saved.id, site, &source.html).await;

    for (position, url) in image_urls.iter().enumerate() {
        let _ = image_store::insert_image_url(&state.db, saved.id, url, position as i64).await;
    }

    // Download any pending images.
    let cached = images::cache_images(&state.db, &state.client, state.store.as_ref(), saved.id).await;
    tracing::info!("add_listing: id={} cached {} new image(s)", saved.id, cached);

    let images = image_store::list_images_with_meta(&state.db, saved.id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {}", e)))?;
    let open_houses = open_house_store::list_open_houses(&state.db, saved.id)
        .await
        .unwrap_or_default();
    Ok(Property::from_stored(saved, images, open_houses))
}

/// Returns `true` for hosts that are known to block programmatic HTTP
/// requests at the infrastructure level (bot-protection CDNs), making
/// HTML scraping impossible without a real browser.
///
/// - **zillow.com** — PerimeterX via CloudFront (`x-px-blocked: 1`)
/// - **realtor.ca** — Imperva Incapsula
fn is_blocked_host(site: parsers::ListingSite) -> bool {
    matches!(site, parsers::ListingSite::Zillow | parsers::ListingSite::Realtor)
}

/// Constructs a blank `StoredProperty` with all fields zeroed/None and mortgage
/// defaults pre-filled.  Used as a base for stub listings when scraping is
/// blocked.  Callers should set the relevant URL field(s) after calling this.
fn blank_stub() -> StoredProperty {
    StoredProperty {
        id: 0,
        search_profile_id: None, // overwritten by the caller before insert
        redfin_url: None,
        realtor_url: None,
        rew_url: None,
        zillow_url: None,
        title: String::new(),
        description: String::new(),
        price: None,
        price_currency: None,
        offer_price: None,
        street_address: None,
        city: None,
        region: None,
        postal_code: None,
        country: None,
        bedrooms: None,
        bathrooms: None,
        sqft: None,
        year_built: None,
        lat: None,
        lon: None,
        created_at: String::new(),
        updated_at: None,
        notes: None,
        parking_total: None,
        parking_garage: None,
        parking_carport: None,
        parking_pad: None,
        land_sqft: None,
        property_tax: None,
        skytrain_station: None,
        skytrain_walk_min: None,
        radiant_floor_heating: None,
        ac: None,
        down_payment_pct: Some(0.20),
        mortgage_interest_rate: Some(0.04),
        amortization_years: Some(25),
        mortgage_monthly: None,
        hoa_monthly: None,
        monthly_total: None,
        monthly_cost: None,
        has_rental_suite: None,
        rental_income: None,
        status: ListingStatus::Interested,
        school_elementary: None,
        school_elementary_rating: None,
        school_middle: None,
        school_middle_rating: None,
        school_secondary: None,
        school_secondary_rating: None,
        property_type: None,
        listed_date: None,
        mls_number: None,
        laundry_in_unit: None,
        source_status: None,
        agent_comment: None,
    }
}
