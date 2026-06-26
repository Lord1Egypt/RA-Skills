//! Collection and lifecycle handlers for listings.
//!
//! - GET    /api/listings      — list all properties
//! - GET    /api/listings/:id  — get a single property
//! - DELETE /api/listings/:id  — delete a property and its images

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    Json,
};
use object_store::{path::Path as ObjectPath, ObjectStoreExt};
use serde::Deserialize;
use tokio::fs;

use crate::images::paths;
use crate::models::property::{ListingStatus, Property};
use crate::store::{image_store, property_store};
use crate::AppState;

#[derive(Deserialize)]
pub struct ListingsQuery {
    /// Comma-separated status values to include, e.g. `status=Interested,Buyable`.
    /// Omit to return all listings.
    pub status: Option<String>,
    /// Filter by search profile id.
    pub search_profile_id: Option<i64>,
}

/// GET /api/listings[?status=Interested,Buyable&search_profile_id=1]
///
/// Returns saved properties, newest first. Optionally filtered by status and/or search.
/// Each record includes cached image metadata (id, local_path, position).
pub(crate) async fn list_listings(
    State(state): State<AppState>,
    Query(params): Query<ListingsQuery>,
) -> Result<Json<Vec<Property>>, (StatusCode, String)> {
    // Parse "Interested,Buyable" → [ListingStatus::Interested, ...]; empty = all.
    let statuses: Vec<ListingStatus> = match &params.status {
        None => vec![],
        Some(s) => s.split(',').filter_map(|v| v.parse().ok()).collect(),
    };

    let listings = property_store::list(&state.db, &statuses, params.search_profile_id).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("DB error: {}", e),
        )
    })?;
    Ok(Json(listings))
}

/// GET /api/listings/:id
///
/// Returns a single listing by ID (includes images and metadata).
pub(crate) async fn get_listing(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<Property>, (StatusCode, String)> {
    let p = property_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {}", e)))?;
    Ok(Json(p))
}

/// DELETE /api/listings/:id
///
/// Deletes a listing: removes image files from the object store, clears the
/// images_cache rows, then removes the listing row itself.
pub(crate) async fn delete_listing(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<StatusCode, (StatusCode, String)> {
    // 1. Delete locally-cached image files from the object store.
    let cached = image_store::list_cached_images(&state.db, id).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("DB error: {}", e),
        )
    })?;

    for img in &cached {
        let object_key = paths::object_key(id, &img.sha256, &img.ext);
        if let Err(e) = state
            .store
            .delete(&ObjectPath::from(object_key.as_str()))
            .await
        {
            tracing::warn!(
                "delete_listing: could not remove image file {}: {}",
                object_key,
                e
            );
            // Continue — file may already be gone; don't block the delete.
        }
    }

    // 2. Remove the per-listing image directory (now empty after step 1).
    let dir = paths::listing_dir(id);
    if let Err(e) = fs::remove_dir(&dir).await {
        tracing::debug!("delete_listing: could not remove image dir {}: {}", dir.display(), e);
    }

    // 3. Remove images_cache rows (no CASCADE on this FK).
    image_store::delete_all_image_records(&state.db, id)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?;

    // 4. Delete the listing row (listing_history cascades automatically).
    property_store::delete(&state.db, id).await.map_err(|e| {
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("DB error: {}", e),
        )
    })?;

    Ok(StatusCode::NO_CONTENT)
}
