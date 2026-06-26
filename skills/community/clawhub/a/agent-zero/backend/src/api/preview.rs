//! Handler for the refresh diff preview endpoint.
//!
//! - GET /api/listings/:id/preview — fetch and parse without saving; returns a
//!   `ResolvedListing` so callers can distinguish a status-only update (off-market)
//!   from a full data refresh and diff accordingly.

use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};

use crate::models::open_house::OpenHouse;
use crate::models::property::Property;
use crate::store::property_store;
use crate::{parsers, AppState};

use super::refresh::{fetch_sources, resolve_parsed_listing, stored_source_urls, ResolvedListing};

/// GET /api/listings/:id/preview
///
/// Fetches and parses a listing without saving — used to build the refresh diff preview.
/// Returns a [`ResolvedListing`]:
/// - `StatusOnly { source_status }` when the page is data-stripped (off-market).
/// - `Full { property }` with the merged property (including freshly parsed open houses
///   at negative fake IDs) when full data is available.
pub(crate) async fn preview_refresh(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<ResolvedListing>, (StatusCode, String)> {
    // ── 1. Load the stored record ──────────────────────────────────────────────
    let stored = property_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {}", e)))?;

    // ── 2. Fetch HTML for each stored source URL ───────────────────────────────
    let stored_urls = stored_source_urls(&stored);
    let sources = fetch_sources(&state, &stored_urls, "preview_refresh", false).await?;

    // ── 3. Parse and resolve ───────────────────────────────────────────────────
    let listing = parsers::parse_multi(&sources).ok_or((
        StatusCode::UNPROCESSABLE_ENTITY,
        "No recognized listing format found in page".to_string(),
    ))?;

    let (resolved, extras) = resolve_parsed_listing(listing, &stored);
    match resolved {
        // ── 3a. Off-market / data-stripped page ───────────────────────────────
        // Only the source_status field would change; return it directly so the
        // caller can show a focused "status-only" diff rather than spurious resets.
        status_only @ ResolvedListing::StatusOnly { .. } => Ok(Json(status_only)),

        // ── 4. Full listing — populate open_houses then return ────────────────
        ResolvedListing::Full { property: preview } => {
            // Attach the freshly parsed open house events so the diff can compare
            // them against the stored ones. Use negative fake IDs (never in DB).
            let parsed_open_houses: Vec<OpenHouse> = extras.unwrap().open_houses
                .into_iter()
                .enumerate()
                .map(|(i, oh)| OpenHouse {
                    id: -(i as i64 + 1),
                    listing_id: stored.id,
                    start_time: oh.start_time,
                    end_time: oh.end_time,
                    visited: false,
                    created_at: String::new(),
                })
                .collect();

            let property = Property { open_houses: parsed_open_houses, ..preview };
            Ok(Json(ResolvedListing::Full { property }))
        }
    }
}
