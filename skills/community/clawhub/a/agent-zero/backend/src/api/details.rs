//! Handlers for editing listing details and reading audit history.
//!
//! - PATCH /api/listings/:id/notes    — update the notes field
//! - PATCH /api/listings/:id/details  — update any user-editable field
//! - GET   /api/listings/:id/history  — field change history

use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use serde::Deserialize;

use crate::fetching::url::parse_listing_url;
use crate::models::history::HistoryEntry;
use crate::models::property::{Property, StoredProperty, UserDetails};
use crate::finance as property_finance;
use crate::store::{history_store, image_store, open_house_store, property_store};
use crate::{parsers, AppState};

/// Validate and strip query params from a URL that must belong to `expected`.
/// Returns the cleaned URL string, or a 400 error describing what went wrong.
fn validate_listing_url(
    url: &str,
    expected: parsers::ListingSite,
) -> Result<String, (StatusCode, String)> {
    let lu = parse_listing_url(url).ok_or_else(|| {
        (
            StatusCode::BAD_REQUEST,
            format!("Invalid URL (must be a http/https {} link): {url}", expected.name()),
        )
    })?;
    if lu.site != expected {
        return Err((
            StatusCode::BAD_REQUEST,
            format!("Expected a {} URL but got a {} URL", expected.name(), lu.site.name()),
        ));
    }
    Ok(lu.url.to_string())
}

#[derive(Deserialize)]
pub struct NotesRequest {
    pub notes: Option<String>,
}

#[derive(Deserialize)]
pub struct SearchIdRequest {
    pub search_profile_id: i64,
}

/// PATCH /api/listings/:id/notes
///
/// Updates the personal notes for a listing. `id` is the property/listing ID.
pub(crate) async fn patch_notes(
    State(state): State<AppState>,
    Path(id): Path<i64>,
    Json(body): Json<NotesRequest>,
) -> Result<StatusCode, (StatusCode, String)> {
    property_store::update_notes(&state.db, id, body.notes.as_deref())
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?;
    Ok(StatusCode::NO_CONTENT)
}

/// PATCH /api/listings/:id/search-profile
///
/// Move a listing to a different search profile (or detach it by passing `null`).
pub(crate) async fn patch_search_profile(
    State(state): State<AppState>,
    Path(id): Path<i64>,
    Json(body): Json<SearchIdRequest>,
) -> Result<StatusCode, (StatusCode, String)> {
    property_store::update_search_profile_id(&state.db, id, body.search_profile_id)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?;
    Ok(StatusCode::NO_CONTENT)
}

/// PATCH /api/listings/:id/details
///
/// Updates user-tracked details for a listing. `id` is the property/listing ID.
/// Records a history entry if the price changed. Returns the updated property.
pub(crate) async fn patch_details(
    State(state): State<AppState>,
    Path(id): Path<i64>,
    Json(body): Json<UserDetails>,
) -> Result<Json<Property>, (StatusCode, String)> {
    // Load the stored record once; used both as the merge base and for price-history comparison.
    let current = property_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {}", e)))?;

    // Merge every provided field from the request body over the stored values.
    // Fields absent from the body (None) are left unchanged.
    let mut updated = StoredProperty::from(current.clone());

    updated.title = body.title.clone().unwrap_or(updated.title.clone());

    if let Some(url) = &body.redfin_url {
        let validated = validate_listing_url(url, parsers::ListingSite::Redfin)?;
        tracing::info!("patch_details: id={} updating redfin_url to {}", id, validated);
        updated.redfin_url = Some(validated);
    }
    if let Some(url) = &body.realtor_url {
        let validated = validate_listing_url(url, parsers::ListingSite::Realtor)?;
        tracing::info!("patch_details: id={} updating realtor_url to {}", id, validated);
        updated.realtor_url = Some(validated);
    }
    if let Some(url) = &body.rew_url {
        let validated = validate_listing_url(url, parsers::ListingSite::Rew)?;
        tracing::info!("patch_details: id={} updating rew_url to {}", id, validated);
        updated.rew_url = Some(validated);
    }
    if let Some(url) = &body.zillow_url {
        let validated = validate_listing_url(url, parsers::ListingSite::Zillow)?;
        tracing::info!("patch_details: id={} updating zillow_url to {}", id, validated);
        updated.zillow_url = Some(validated);
    }

    updated.price = body.price.or(updated.price);
    updated.price_currency = body
        .price_currency
        .clone()
        .or(updated.price_currency.clone());
    updated.offer_price = body.offer_price.or(updated.offer_price);
    updated.bedrooms = body.bedrooms.or(updated.bedrooms);
    updated.bathrooms = body.bathrooms.or(updated.bathrooms);
    updated.sqft = body.sqft.or(updated.sqft);
    updated.year_built = body.year_built.or(updated.year_built);
    updated.parking_total = body.parking_total.or(updated.parking_total);
    updated.parking_garage = body.parking_garage.or(updated.parking_garage);
    updated.parking_carport = body.parking_carport.or(updated.parking_carport);
    updated.parking_pad = body.parking_pad.or(updated.parking_pad);
    if body.parking_garage.is_some() || body.parking_carport.is_some() || body.parking_pad.is_some()
    {
        updated.parking_total = Some(
            updated.parking_garage.unwrap_or(0)
                + updated.parking_carport.unwrap_or(0)
                + updated.parking_pad.unwrap_or(0),
        );
    }
    updated.land_sqft = body.land_sqft.or(updated.land_sqft);
    updated.property_tax = body.property_tax.or(updated.property_tax);
    updated.skytrain_station = body
        .skytrain_station
        .clone()
        .or(updated.skytrain_station.clone());
    updated.skytrain_walk_min = body.skytrain_walk_min.or(updated.skytrain_walk_min);
    updated.radiant_floor_heating = body.radiant_floor_heating.or(updated.radiant_floor_heating);
    updated.ac = body.ac.or(updated.ac);
    updated.down_payment_pct = body.down_payment_pct.or(updated.down_payment_pct);
    updated.mortgage_interest_rate = body
        .mortgage_interest_rate
        .or(updated.mortgage_interest_rate);
    updated.amortization_years = body.amortization_years.or(updated.amortization_years);
    updated.hoa_monthly = body.hoa_monthly.or(updated.hoa_monthly);
    updated.monthly_total = body.monthly_total.or(updated.monthly_total);
    updated.monthly_cost = body.monthly_cost.or(updated.monthly_cost);
    updated.has_rental_suite = body.has_rental_suite.or(updated.has_rental_suite);
    updated.rental_income = body.rental_income.or(updated.rental_income);
    if let Some(s) = body.status {
        updated.status = s;
    }
    updated.school_elementary = body
        .school_elementary
        .clone()
        .or(updated.school_elementary.clone());
    updated.school_elementary_rating = body
        .school_elementary_rating
        .or(updated.school_elementary_rating);
    updated.school_middle = body.school_middle.clone().or(updated.school_middle.clone());
    updated.school_middle_rating = body.school_middle_rating.or(updated.school_middle_rating);
    updated.school_secondary = body
        .school_secondary
        .clone()
        .or(updated.school_secondary.clone());
    updated.school_secondary_rating = body
        .school_secondary_rating
        .or(updated.school_secondary_rating);
    updated.property_type = body.property_type.clone().or(updated.property_type.clone());
    updated.laundry_in_unit = body.laundry_in_unit.or(updated.laundry_in_unit);
    updated.mls_number = body.mls_number.clone().or(updated.mls_number.clone());

    let mut updated = property_store::update_by_id(&state.db, id, &updated)
        .await
        .map_err(|e| {
            let msg = e.to_string();
            if msg.contains("UNIQUE constraint failed: listings.redfin_url") {
                (StatusCode::CONFLICT, "This Redfin URL is already linked to another listing".to_string())
            } else if msg.contains("UNIQUE constraint failed: listings.realtor_url") {
                (StatusCode::CONFLICT, "This Realtor URL is already linked to another listing".to_string())
            } else if msg.contains("UNIQUE constraint failed: listings.rew_url") {
                (StatusCode::CONFLICT, "This REW URL is already linked to another listing".to_string())
            } else if msg.contains("UNIQUE constraint failed: listings.zillow_url") {
                (StatusCode::CONFLICT, "This Zillow URL is already linked to another listing".to_string())
            } else {
                (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {}", e))
            }
        })?;

    // Recompute monthly_total/monthly_cost from the freshly saved values.
    let down_pct = updated.down_payment_pct.unwrap_or(0.20);
    let rate = updated.mortgage_interest_rate.unwrap_or(0.05);
    let years = updated.amortization_years.unwrap_or(25);
    let finance = property_finance::compute(
        updated.price, updated.offer_price, down_pct, rate, years,
        updated.property_tax, updated.hoa_monthly,
    );
    updated.mortgage_monthly = finance.mortgage_monthly;
    updated.monthly_total = finance.monthly_total;
    updated.monthly_cost = finance.monthly_cost;

    let _ = sqlx::query(
        "UPDATE listings SET mortgage_monthly = ?, monthly_total = ?, monthly_cost = ? WHERE id = ?",
    )
    .bind(updated.mortgage_monthly)
    .bind(updated.monthly_total)
    .bind(updated.monthly_cost)
        .bind(id)
        .execute(&state.db)
        .await;

    if current.price != updated.price {
        let old = current.price.map(|v| v.to_string());
        let new = updated.price.map(|v| v.to_string());
        let _ = history_store::insert_change(
            &state.db,
            id,
            crate::models::history::HistoryField::Price,
            old.as_deref(),
            new.as_deref(),
        )
        .await;
    }

    // Re-attach images and open houses (update_by_id doesn't load them).
    let images = image_store::list_images_with_meta(&state.db, id)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?;
    let open_houses = open_house_store::list_open_houses(&state.db, id)
        .await
        .unwrap_or_default();

    Ok(Json(Property::from_stored(updated, images, open_houses)))
}

/// GET /api/listings/:id/history
///
/// Returns price/field change history for a listing. `id` is the property/listing ID.
pub(crate) async fn get_history(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<Vec<HistoryEntry>>, (StatusCode, String)> {
    let entries = history_store::list_history(&state.db, id).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("DB error: {}", e),
        )
    })?;
    Ok(Json(entries))
}
