use crate::images;
use crate::fetching::fetch::fetch_html;
use crate::fetching::html_snapshots::save_listing_html;
use crate::fetching::url::parse_listing_url;
use crate::models::open_house::OpenHouseEvent;
use crate::models::property::{Property, SourceStatus, StoredProperty};
use crate::parsers;
use crate::finance as property_finance;
use crate::store::{history_store, image_store, open_house_store, property_store};
use crate::AppState;
use axum::http::StatusCode;
use axum::{
    extract::{Path, State},
    Json,
};
use serde::{Deserialize, Serialize};

/// Returns `true` when the stored title has been set by the user and should be
/// preserved during a refresh. An empty string means the user never set one (or
/// cleared it), so the parser title is allowed through.
fn is_title_exist(title: &str) -> bool {
    !title.is_empty()
}

/// Collects all non-`None` source URLs from a stored property in a consistent
/// order (Redfin → Realtor → REW → Zillow). The resulting slice is passed to
/// [`fetch_sources`] to re-fetch and re-parse during a refresh or preview.
pub(crate) fn stored_source_urls(stored: &Property) -> Vec<String> {
    [
        stored.redfin_url.clone(),
        stored.realtor_url.clone(),
        stored.rew_url.clone(),
        stored.zillow_url.clone(),
    ]
    .into_iter()
    .flatten()
    .collect()
}

pub(crate) async fn fetch_sources(
    state: &AppState,
    urls: &[String],
    context: &str,
    log_success: bool,
) -> Result<Vec<parsers::SourceInput>, (StatusCode, String)> {
    if urls.is_empty() {
        return Err((
            StatusCode::BAD_REQUEST,
            "No source URL stored for this listing".to_string(),
        ));
    }

    let mut sources: Vec<parsers::SourceInput> = Vec::new();
    for url in urls {
        let parsed_url = parse_listing_url(url).ok_or((
            StatusCode::BAD_REQUEST,
            format!("Invalid stored URL: {url}"),
        ))?.url;
        match fetch_html(&state.client, &parsed_url).await {
            Ok(html) => {
                if log_success {
                    tracing::info!(
                        "{}: fetched source url={}",
                        context,
                        parsed_url.as_str()
                    );
                }
                sources.push(parsers::SourceInput {
                    url: parsed_url.to_string(),
                    html,
                });
            }
            Err(e) => {
                tracing::warn!("{}: failed to fetch {}: {}", context, url, e);
                sources.push(parsers::SourceInput {
                    url: parsed_url.to_string(),
                    html: String::new(),
                });
            }
        }
    }

    Ok(sources)
}

/// Merges a freshly parsed property with the stored record into the final value
/// that gets written back to the DB (or returned as a preview).
///
/// Every field of [`StoredProperty`] is listed explicitly so that adding a new field
/// to the struct produces a compile error here, forcing a conscious merge decision.
///
/// The three merge rules used below are:
/// - **Identity / user-owned** — always taken from `stored`; the parser has no
///   knowledge of these (e.g. `search_profile_id`, `status`, skytrain data).
/// - **Parser wins, stored as fallback** — parser value used when present;
///   stored value kept when the parser returns `None` (schools, HOA fee).
/// - **Parser wins** — everything else; the fresh parse is the source of truth.
///
/// `id` is passed separately because callers know the DB row id while the
/// parsed struct always carries `0`.
fn merge_with_stored(parsed_listing: StoredProperty, stored_listing: &StoredProperty, id: i64) -> StoredProperty {
    // Pre-compute fields that are both stored in the struct and fed into the
    // mortgage calculation, so each value is stated exactly once.
    let hoa_monthly = parsed_listing.hoa_monthly.or(stored_listing.hoa_monthly);
    let property_tax = parsed_listing.property_tax.or(stored_listing.property_tax);
    let down_pct = stored_listing.down_payment_pct.unwrap_or(0.20);
    let rate = stored_listing.mortgage_interest_rate.unwrap_or(0.04);
    let years = stored_listing.amortization_years.unwrap_or(25);
    let finance = property_finance::compute(
        parsed_listing.price,
        stored_listing.offer_price,
        down_pct,
        rate,
        years,
        property_tax,
        hoa_monthly,
    );

    StoredProperty {
        // ── Identity ──────────────────────────────────────────────────────────
        // These fields have no representation in the parsed HTML.
        // search_profile_id must come from stored; writing the struct default (0)
        // violates the FK constraint on the search_profiles table.
        id,
        search_profile_id: stored_listing.search_profile_id,

        // ── Source URLs ───────────────────────────────────────────────────────
        // Users may manually link additional sources; preserve them all.
        redfin_url: stored_listing.redfin_url.clone(),
        realtor_url: stored_listing.realtor_url.clone(),
        rew_url: stored_listing.rew_url.clone(),
        zillow_url: stored_listing.zillow_url.clone(),

        // ── User-owned: parser never produces these ───────────────────────────
        status: stored_listing.status,
        notes: stored_listing.notes.clone(),
        offer_price: stored_listing.offer_price,
        skytrain_station: stored_listing.skytrain_station.clone(),
        skytrain_walk_min: stored_listing.skytrain_walk_min,
        has_rental_suite: stored_listing.has_rental_suite,
        rental_income: stored_listing.rental_income,

        // ── User-set mortgage parameters ──────────────────────────────────────
        down_payment_pct: Some(down_pct),
        mortgage_interest_rate: Some(rate),
        amortization_years: Some(years),

        // ── Parser wins, stored as fallback ───────────────────────────────────
        title: if is_title_exist(&stored_listing.title) { stored_listing.title.clone() } else { parsed_listing.title },
        school_elementary: parsed_listing.school_elementary.or(stored_listing.school_elementary.clone()),
        school_elementary_rating: parsed_listing.school_elementary_rating.or(stored_listing.school_elementary_rating),
        school_middle: parsed_listing.school_middle.or(stored_listing.school_middle.clone()),
        school_middle_rating: parsed_listing.school_middle_rating.or(stored_listing.school_middle_rating),
        school_secondary: parsed_listing.school_secondary.or(stored_listing.school_secondary.clone()),
        school_secondary_rating: parsed_listing.school_secondary_rating.or(stored_listing.school_secondary_rating),
        hoa_monthly,

        // ── Parser wins, stored as fallback ───────────────────────────────────
        // Fresh parse is the source of truth; stored value is kept when parser
        // returns None so that manually-entered or previously-parsed data is
        // never silently erased by a page that temporarily omits a field.
        description: parsed_listing.description,
        price: parsed_listing.price.or(stored_listing.price),
        price_currency: parsed_listing.price_currency.or(stored_listing.price_currency.clone()),
        street_address: parsed_listing.street_address.or(stored_listing.street_address.clone()),
        city: parsed_listing.city.or(stored_listing.city.clone()),
        region: parsed_listing.region.or(stored_listing.region.clone()),
        postal_code: parsed_listing.postal_code.or(stored_listing.postal_code.clone()),
        country: parsed_listing.country.or(stored_listing.country.clone()),
        lat: parsed_listing.lat.or(stored_listing.lat),
        lon: parsed_listing.lon.or(stored_listing.lon),
        property_type: parsed_listing.property_type.or(stored_listing.property_type.clone()),
        bedrooms: parsed_listing.bedrooms.or(stored_listing.bedrooms),
        bathrooms: parsed_listing.bathrooms.or(stored_listing.bathrooms),
        sqft: parsed_listing.sqft.or(stored_listing.sqft),
        land_sqft: parsed_listing.land_sqft.or(stored_listing.land_sqft),
        year_built: parsed_listing.year_built.or(stored_listing.year_built),
        parking_total: parsed_listing.parking_total.or(stored_listing.parking_total),
        parking_garage: parsed_listing.parking_garage.or(stored_listing.parking_garage),
        parking_carport: parsed_listing.parking_carport.or(stored_listing.parking_carport),
        parking_pad: parsed_listing.parking_pad.or(stored_listing.parking_pad),
        radiant_floor_heating: parsed_listing.radiant_floor_heating.or(stored_listing.radiant_floor_heating),
        ac: parsed_listing.ac.or(stored_listing.ac),
        laundry_in_unit: parsed_listing.laundry_in_unit.or(stored_listing.laundry_in_unit),
        property_tax,
        mls_number: parsed_listing.mls_number.or(stored_listing.mls_number.clone()),
        // Preserve the original listed_date; a new MLS number means a relist,
        // which is captured in history, not by overwriting the first-seen date.
        listed_date: stored_listing.listed_date.clone().or(parsed_listing.listed_date),

        // ── Computed ──────────────────────────────────────────────────────────
        mortgage_monthly: finance.mortgage_monthly,
        monthly_total: finance.monthly_total,
        monthly_cost: finance.monthly_cost,

        // ── Source status ─────────────────────────────────────────────────────
        // Use the parser's extracted status (e.g. "Pending", "Off Market").
        // None means actively for sale — also clears any stale off-market status.
        source_status: parsed_listing.source_status.clone(),

        // ── Agent review ──────────────────────────────────────────────────────
        // Preserve the agent's comment and never overwrite it on refresh.
        agent_comment: stored_listing.agent_comment.clone(),

        // ── System metadata ───────────────────────────────────────────────────
        // Neither value affects the UPDATE: created_at is not in the SET clause,
        // and updated_at is overwritten with datetime('now') by the SQL.
        // The correct values come back from the fetch_one_by_id re-read in update_by_id.
        created_at: stored_listing.created_at.clone(),
        updated_at: stored_listing.updated_at.clone(),
    }
}

/// The outcome of resolving a freshly parsed listing against the stored record.
/// Serializes as a tagged JSON object (`"kind": "status_only"` / `"kind": "full"`).
#[derive(Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum ResolvedListing {
    /// The parsed page has a source_status (e.g. Pending, OffMarket) — treat as
    /// data-stripped and preserve all stored fields.
    StatusOnly {
        source_status: SourceStatus,
    },
    /// The parsed page has full listing data — the merged property ready to use.
    Full {
        property: Property,
    },
}

/// Extra data produced by parsing that lives outside `Property` and is only
/// needed by `refresh_listing` (not the preview path).
pub(crate) struct ParsedExtras {
    pub image_urls: Vec<String>,
    pub open_houses: Vec<OpenHouseEvent>,
    pub parsed_listed_date: Option<String>,
}

/// Applies merge and off-market guard logic to a freshly parsed listing.
/// Returns the wire-ready `ResolvedListing` and, for the `Full` path, the
/// accompanying `ParsedExtras` that `refresh_listing` needs for DB writes.
pub(crate) fn resolve_parsed_listing(
    listing: parsers::ParsedListing,
    stored: &Property,
) -> (ResolvedListing, Option<ParsedExtras>) {
    if let Some(source_status) = listing.property.source_status {
        // The page has a source_status (e.g. Pending, OffMarket) — treat as data-stripped
        // and preserve all stored fields rather than overwriting with potentially incomplete
        // parsed data.
        return (ResolvedListing::StatusOnly { source_status }, None);
    }
    let extras = ParsedExtras {
        image_urls: listing.image_urls,
        open_houses: listing.open_houses,
        parsed_listed_date: listing.property.listed_date.clone(),
    };
    let stored_base = StoredProperty::from(stored.clone());
    let merged = merge_with_stored(listing.property, &stored_base, stored.id);
    let property = Property::from_stored(merged, vec![], vec![]);
    (ResolvedListing::Full { property }, Some(extras))
}

/// Writes only the `source_status` field to the DB and returns the updated
/// property. Used when the parsed page is data-stripped (off-market) so that
/// all other stored data is preserved.
async fn status_only_refresh(
    db: &sqlx::SqlitePool,
    id: i64,
    stored: &Property,
    new_status: Option<SourceStatus>,
) -> Result<Json<Property>, (StatusCode, String)> {
    if stored.source_status != new_status {
        let old_s = stored.source_status.as_ref().map(|s| s.to_string());
        let new_s = new_status.as_ref().map(|s| s.to_string());
        let _ = history_store::insert_change(
            db, id,
            crate::models::history::HistoryField::SourceStatus,
            old_s.as_deref(), new_s.as_deref(),
        ).await;
    }
    let new_s = new_status.as_ref().map(|s| s.to_string());
    let saved = property_store::update_source_status(db, id, new_s.as_deref())
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    let images = image_store::list_images_with_meta(db, id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    let open_houses = open_house_store::list_open_houses(db, id)
        .await
        .unwrap_or_default();
    Ok(Json(Property::from_stored(saved, images, open_houses)))
}

/// PUT /api/listings/:id/refresh
///
/// Re-fetches the stored source URLs, re-parses, and saves the updated data.
/// The parsed result is merged with the stored record via [`merge_with_stored`]
/// before saving: user-owned fields survive, parser fields are overwritten, and
/// shared fields (schools, HOA) fall back to the stored value when the parser
/// returns nothing.
pub(crate) async fn refresh_listing(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<Property>, (StatusCode, String)> {
    // ── 1. Load the stored record ──────────────────────────────────────────────
    let stored = property_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {}", e)))?;

    // ── 2. Fetch HTML for each stored source URL ───────────────────────────────
    let source_urls = stored_source_urls(&stored);
    let sources = fetch_sources(&state, &source_urls, "refresh_listing", true).await?;

    // ── 3. Parse ───────────────────────────────────────────────────────────────
    // Save raw HTML snapshots for offline inspection / parser backfills.
    for source in &sources {
        if let Some(site) = parsers::ListingSite::from_url(&source.url) {
            save_listing_html(id, site, &source.html).await;
        }
    }

    let Some(listing) = parsers::parse_multi(&sources) else {
        // No recognised listing format — the property is likely off-market or removed.
        tracing::info!("refresh_listing: id={} no listing found — marking OffMarket", id);
        return status_only_refresh(&state.db, id, &stored, Some(SourceStatus::OffMarket)).await;
    };

    // ── 4. Resolve parsed result ───────────────────────────────────────────────
    let (resolved, extras) = resolve_parsed_listing(listing, &stored);
    match resolved {
        ResolvedListing::StatusOnly { source_status: new_status } => {
            tracing::info!(
                "refresh_listing: id={} data-stripped page (source_status={:?}), skipping full update",
                id, new_status
            );
            status_only_refresh(&state.db, id, &stored, Some(new_status)).await
        }

        ResolvedListing::Full { property: updated } => {
            let ParsedExtras { image_urls, open_houses, parsed_listed_date } = extras.unwrap();
            tracing::info!(
                "refresh_listing: parse result property_tax={:?}, price={:?}",
                updated.property_tax,
                updated.price
            );

            // ── 5. Record history for changed fields ──────────────────────────
            if stored.price != updated.price {
                let old = stored.price.map(|v| v.to_string());
                let new = updated.price.map(|v| v.to_string());
                let _ = history_store::insert_change(
                    &state.db, id,
                    crate::models::history::HistoryField::Price,
                    old.as_deref(), new.as_deref(),
                ).await;
            }
            if stored.mls_number != updated.mls_number {
                let _ = history_store::insert_change(
                    &state.db, id,
                    crate::models::history::HistoryField::MlsNumber,
                    stored.mls_number.as_deref(), updated.mls_number.as_deref(),
                ).await;
                if stored.listed_date.as_deref() != parsed_listed_date.as_deref() {
                    let _ = history_store::insert_change(
                        &state.db, id,
                        crate::models::history::HistoryField::ListedDate,
                        stored.listed_date.as_deref(), parsed_listed_date.as_deref(),
                    ).await;
                }
            }
            if stored.source_status != updated.source_status {
                let old_ss = stored.source_status.as_ref().map(|s| s.to_string());
                let new_ss = updated.source_status.as_ref().map(|s| s.to_string());
                let _ = history_store::insert_change(
                    &state.db, id,
                    crate::models::history::HistoryField::SourceStatus,
                    old_ss.as_deref(), new_ss.as_deref(),
                ).await;
            }

            // ── 6. Persist ────────────────────────────────────────────────────
            let updated_stored = StoredProperty::from(updated);
            let saved = property_store::update_by_id(&state.db, id, &updated_stored)
                .await
                .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
            tracing::info!(
                "refresh_listing: saved listing id={} property_tax={:?} price={:?}",
                saved.id, saved.property_tax, saved.price
            );

            // ── 7. Upsert open house events ───────────────────────────────────
            if !open_houses.is_empty() {
                if let Err(e) = open_house_store::upsert_open_houses(&state.db, id, &open_houses).await {
                    tracing::warn!("refresh_listing: failed to save open houses for id={}: {}", id, e);
                }
            }

            // ── 8. Refresh image cache ────────────────────────────────────────
            tracing::info!("refresh_listing: id={} registering {} image URL(s)", id, image_urls.len());
            for (position, url) in image_urls.iter().enumerate() {
                let _ = image_store::insert_image_url(&state.db, id, url, position as i64).await;
            }
            let cached = images::cache_images(&state.db, &state.client, state.store.as_ref(), id).await;
            tracing::info!("refresh_listing: id={} cached {} new image(s)", id, cached);

            // ── 9. Return with image metadata ─────────────────────────────────
            let images = image_store::list_images_with_meta(&state.db, saved.id)
                .await
                .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
            let open_houses = open_house_store::list_open_houses(&state.db, saved.id)
                .await
                .unwrap_or_default();
            Ok(Json(Property::from_stored(saved, images, open_houses)))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::models::property::ListingStatus;

    /// Minimal valid `StoredProperty` with every field at its zero/None value.
    /// Tests should override only the fields they care about.
    fn base_stored() -> StoredProperty {
        StoredProperty {
            id: 0,
            search_profile_id: Some(1),
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
            lat: None,
            lon: None,
            property_type: None,
            bedrooms: None,
            bathrooms: None,
            sqft: None,
            land_sqft: None,
            year_built: None,
            parking_total: None,
            parking_garage: None,
            parking_carport: None,
            parking_pad: None,
            radiant_floor_heating: None,
            ac: None,
            laundry_in_unit: None,
            skytrain_station: None,
            skytrain_walk_min: None,
            property_tax: None,
            hoa_monthly: None,
            down_payment_pct: None,
            mortgage_interest_rate: None,
            amortization_years: None,
            mortgage_monthly: None,
            monthly_total: None,
            monthly_cost: None,
            has_rental_suite: None,
            rental_income: None,
            school_elementary: None,
            school_elementary_rating: None,
            school_middle: None,
            school_middle_rating: None,
            school_secondary: None,
            school_secondary_rating: None,
            redfin_url: None,
            realtor_url: None,
            rew_url: None,
            zillow_url: None,
            mls_number: None,
            listed_date: None,
            source_status: None,
            status: ListingStatus::Interested,
            notes: None,
            agent_comment: None,
            created_at: String::new(),
            updated_at: None,
        }
    }

    fn base_property() -> Property {
        Property::from_stored(base_stored(), vec![], vec![])
    }

    // ── is_title_exist ────────────────────────────────────────────────────────

    #[test]
    fn test_is_title_exist_empty_string() {
        assert!(!is_title_exist(""));
    }

    #[test]
    fn test_is_title_exist_non_empty_string() {
        assert!(is_title_exist("123 Main St"));
    }

    // ── stored_source_urls ────────────────────────────────────────────────────

    #[test]
    fn test_stored_source_urls_all_set() {
        let p = Property {
            redfin_url: Some("https://redfin.ca/1".to_string()),
            realtor_url: Some("https://realtor.ca/1".to_string()),
            rew_url: Some("https://rew.ca/1".to_string()),
            zillow_url: Some("https://zillow.com/1".to_string()),
            ..base_property()
        };
        let urls = stored_source_urls(&p);
        assert_eq!(urls.len(), 4);
        assert_eq!(urls[0], "https://redfin.ca/1");
        assert_eq!(urls[1], "https://realtor.ca/1");
        assert_eq!(urls[2], "https://rew.ca/1");
        assert_eq!(urls[3], "https://zillow.com/1");
    }

    #[test]
    fn test_stored_source_urls_partial() {
        let p = Property {
            redfin_url: Some("https://redfin.ca/1".to_string()),
            zillow_url: Some("https://zillow.com/1".to_string()),
            ..base_property()
        };
        let urls = stored_source_urls(&p);
        assert_eq!(urls.len(), 2);
        assert_eq!(urls[0], "https://redfin.ca/1");
        assert_eq!(urls[1], "https://zillow.com/1");
    }

    #[test]
    fn test_stored_source_urls_none() {
        let urls = stored_source_urls(&base_property());
        assert!(urls.is_empty());
    }

    // ── merge_with_stored ─────────────────────────────────────────────────────

    #[test]
    fn test_merge_identity_fields_from_stored() {
        let parsed = StoredProperty {
            redfin_url: Some("https://wrong.com".to_string()),
            search_profile_id: None,
            ..base_stored()
        };
        let stored = StoredProperty {
            redfin_url: Some("https://redfin.ca/correct".to_string()),
            realtor_url: Some("https://realtor.ca/correct".to_string()),
            rew_url: None,
            zillow_url: Some("https://zillow.com/correct".to_string()),
            search_profile_id: Some(3),
            ..base_stored()
        };

        let result = merge_with_stored(parsed, &stored, 42);

        assert_eq!(result.id, 42);
        assert_eq!(result.redfin_url.as_deref(), Some("https://redfin.ca/correct"));
        assert_eq!(result.realtor_url.as_deref(), Some("https://realtor.ca/correct"));
        assert_eq!(result.rew_url, None);
        assert_eq!(result.zillow_url.as_deref(), Some("https://zillow.com/correct"));
    }

    /// Regression: parser produces search_profile_id = 0 (struct default),
    /// which has no matching row in search_profiles → FK constraint failure.
    #[test]
    fn test_merge_preserves_search_profile_id() {
        let parsed = StoredProperty { search_profile_id: None, ..base_stored() };
        let stored = StoredProperty { search_profile_id: Some(5), ..base_stored() };

        let result = merge_with_stored(parsed, &stored, 1);

        assert_eq!(result.search_profile_id, Some(5));
    }

    #[test]
    fn test_merge_user_owned_fields_from_stored() {
        let parsed = StoredProperty {
            status: ListingStatus::Interested,
            skytrain_station: None,
            skytrain_walk_min: None,
            has_rental_suite: None,
            rental_income: None,
            offer_price: None,
            notes: None,
            ..base_stored()
        };
        let stored = StoredProperty {
            status: ListingStatus::Buyable,
            skytrain_station: Some("Main St".to_string()),
            skytrain_walk_min: Some(5),
            has_rental_suite: Some(true),
            rental_income: Some(1500),
            offer_price: Some(800_000),
            notes: Some("Great location".to_string()),
            ..base_stored()
        };

        let result = merge_with_stored(parsed, &stored, 1);

        assert_eq!(result.status, ListingStatus::Buyable);
        assert_eq!(result.skytrain_station.as_deref(), Some("Main St"));
        assert_eq!(result.skytrain_walk_min, Some(5));
        assert_eq!(result.has_rental_suite, Some(true));
        assert_eq!(result.rental_income, Some(1500));
        assert_eq!(result.offer_price, Some(800_000));
        assert_eq!(result.notes.as_deref(), Some("Great location"));
    }

    #[test]
    fn test_merge_parser_fields_win() {
        let parsed = StoredProperty {
            price: Some(1_200_000),
            bedrooms: Some(4),
            bathrooms: Some(3),
            property_tax: Some(7_000),
            ..base_stored()
        };

        let result = merge_with_stored(parsed, &base_stored(), 1);

        assert_eq!(result.price, Some(1_200_000));
        assert_eq!(result.bedrooms, Some(4));
        assert_eq!(result.bathrooms, Some(3));
        assert_eq!(result.property_tax, Some(7_000));
    }

    #[test]
    fn test_merge_school_parser_wins_over_stored() {
        let parsed = StoredProperty {
            school_elementary: Some("Parser Elementary".to_string()),
            school_elementary_rating: Some(9.0),
            ..base_stored()
        };
        let stored = StoredProperty {
            school_elementary: Some("Stored Elementary".to_string()),
            school_elementary_rating: Some(7.0),
            ..base_stored()
        };

        let result = merge_with_stored(parsed, &stored, 1);

        assert_eq!(result.school_elementary.as_deref(), Some("Parser Elementary"));
        assert_eq!(result.school_elementary_rating, Some(9.0));
    }

    #[test]
    fn test_merge_school_stored_fallback_when_parser_empty() {
        let stored = StoredProperty {
            school_elementary: Some("Stored Elementary".to_string()),
            school_elementary_rating: Some(7.0),
            school_middle: Some("Stored Middle".to_string()),
            school_middle_rating: Some(6.5),
            school_secondary: Some("Stored Secondary".to_string()),
            school_secondary_rating: Some(8.0),
            ..base_stored()
        };

        let result = merge_with_stored(base_stored(), &stored, 1);

        assert_eq!(result.school_elementary.as_deref(), Some("Stored Elementary"));
        assert_eq!(result.school_elementary_rating, Some(7.0));
        assert_eq!(result.school_middle.as_deref(), Some("Stored Middle"));
        assert_eq!(result.school_middle_rating, Some(6.5));
        assert_eq!(result.school_secondary.as_deref(), Some("Stored Secondary"));
        assert_eq!(result.school_secondary_rating, Some(8.0));
    }

    #[test]
    fn test_merge_hoa_parser_wins() {
        let parsed = StoredProperty { hoa_monthly: Some(500), ..base_stored() };
        let stored = StoredProperty { hoa_monthly: Some(300), ..base_stored() };

        assert_eq!(merge_with_stored(parsed, &stored, 1).hoa_monthly, Some(500));
    }

    #[test]
    fn test_merge_hoa_stored_fallback_when_parser_empty() {
        let stored = StoredProperty { hoa_monthly: Some(300), ..base_stored() };

        assert_eq!(merge_with_stored(base_stored(), &stored, 1).hoa_monthly, Some(300));
    }

    #[test]
    fn test_merge_title_preserved_when_user_set() {
        let parsed = StoredProperty { title: "Parser Title".to_string(), ..base_stored() };
        let stored = StoredProperty { title: "User Title".to_string(), ..base_stored() };

        assert_eq!(merge_with_stored(parsed, &stored, 1).title, "User Title");
    }

    #[test]
    fn test_merge_title_uses_parser_when_stored_empty() {
        let parsed = StoredProperty { title: "Parser Title".to_string(), ..base_stored() };

        assert_eq!(merge_with_stored(parsed, &base_stored(), 1).title, "Parser Title");
    }
}
