//! GET /api/parse — fetch a URL and return raw parsed fields without saving to the DB.

use axum::{
    extract::{Query, State},
    http::StatusCode,
    Json,
};
use scraper::Html;
use std::collections::HashMap;

use crate::parsers::{
    extract_description, extract_images, extract_json_ld, extract_title, meta_map, ParseResult,
};
use crate::fetching::fetch::fetch_html;
use crate::fetching::url::parse_listing_url;
use crate::AppState;

/// GET /api/parse?url=<url>
///
/// Fetches the given URL and runs all parsers, returning the raw parsed fields
/// (title, description, images, JSON-LD, meta tags). Does not write to the DB.
pub(crate) async fn parse(
    State(state): State<AppState>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<Json<ParseResult>, (StatusCode, String)> {
    let url = params.get("url").ok_or((
        StatusCode::BAD_REQUEST,
        "Missing 'url' query parameter".to_string(),
    ))?;
    let url = url.trim();
    let parsed = parse_listing_url(url).ok_or((StatusCode::BAD_REQUEST, "Invalid or unsupported listing URL".to_string()))?.url;

    let html = fetch_html(&state.client, &parsed).await.map_err(|e| {
        (
            StatusCode::BAD_GATEWAY,
            format!("Failed to fetch URL: {}", e),
        )
    })?;

    let document = Html::parse_document(&html);
    let json_ld = extract_json_ld(&document);
    let meta = meta_map(&document);
    let title = extract_title(&document);
    let description = extract_description(&document);
    let images = extract_images(&document);

    Ok(Json(ParseResult {
        url: parsed.to_string(),
        title,
        description,
        images,
        raw_json_ld: json_ld,
        meta,
    }))
}
