//! DELETE /api/listings/:id/images/:image_id — remove a single cached image.

use axum::{
    extract::{Path, State},
    http::StatusCode,
};
use object_store::{path::Path as ObjectPath, ObjectStoreExt};
use tokio::fs;

use crate::images::paths;
use crate::store::image_store;
use crate::AppState;

/// DELETE /api/listings/:id/images/:image_id
///
/// Removes a single cached image: deletes the file from the object store and
/// the row from `images_cache`. Silently removes the per-listing directory if
/// it becomes empty.
pub(crate) async fn delete_image(
    State(state): State<AppState>,
    Path((listing_id, image_id)): Path<(i64, i64)>,
) -> Result<StatusCode, (StatusCode, String)> {
    // Verify the image exists and belongs to this listing; get sha256+ext if downloaded.
    let image_ext = image_store::get_image_ext(&state.db, image_id, listing_id)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?
        .ok_or((StatusCode::NOT_FOUND, "Image not found".to_string()))?;

    // Delete the file from the object store when it was successfully downloaded.
    if let Some((sha256, ext)) = image_ext {
        let object_key = paths::object_key(listing_id, &sha256, &ext);
        if let Err(e) = state
            .store
            .delete(&ObjectPath::from(object_key.as_str()))
            .await
        {
            tracing::warn!("Failed to delete image file {}: {}", object_key, e);
            // Proceed to remove the DB record even if file deletion fails.
        }
    }

    image_store::delete_image_record(&state.db, image_id, listing_id)
        .await
        .map_err(|e| {
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("DB error: {}", e),
            )
        })?;

    // If no images remain for this listing, remove the empty per-listing directory.
    let dir = paths::listing_dir(listing_id);
    if let Err(e) = fs::remove_dir(&dir).await {
        // Not empty (other images remain) or already gone — both are fine.
        tracing::debug!("Could not remove image dir {}: {}", dir.display(), e);
    }

    Ok(StatusCode::NO_CONTENT)
}
