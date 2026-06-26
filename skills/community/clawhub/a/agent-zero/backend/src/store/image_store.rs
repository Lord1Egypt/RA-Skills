use crate::images::paths;
use crate::models::image::{CachedImage, ImageEntry};
use sqlx::{Row, SqlitePool};

/// All successfully cached images for a listing (used for SHA-256 / phash dedup).
pub async fn list_cached_images(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<Vec<CachedImage>, sqlx::Error> {
    let rows = sqlx::query(
        "SELECT sha256, phash, ext FROM images_cache
         WHERE listing_id = ? AND ext IS NOT NULL",
    )
    .bind(listing_id)
    .fetch_all(pool)
    .await?;

    Ok(rows
        .iter()
        .map(|r| CachedImage {
            sha256: r.get("sha256"),
            phash: r.get("phash"),
            ext: r.get("ext"),
        })
        .collect())
}

/// Register an image URL for a listing at a given position.
/// If the URL already exists, its position is updated to reflect the latest
/// parser ordering. sha256/phash/ext are left unchanged on conflict.
pub async fn insert_image_url(
    pool: &SqlitePool,
    listing_id: i64,
    source_url: &str,
    position: i64,
) -> Result<(), sqlx::Error> {
    sqlx::query(
        "INSERT INTO images_cache (listing_id, source_url, position, created_at)
         VALUES (?, ?, ?, datetime('now'))
         ON CONFLICT(listing_id, source_url) DO UPDATE SET position = excluded.position",
    )
    .bind(listing_id)
    .bind(source_url)
    .bind(position)
    .execute(pool)
    .await?;
    Ok(())
}

/// URLs that have been registered but not yet downloaded (ext IS NULL).
pub async fn list_pending_image_urls(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<Vec<String>, sqlx::Error> {
    let rows = sqlx::query(
        "SELECT source_url FROM images_cache
         WHERE listing_id = ? AND ext IS NULL ORDER BY position",
    )
    .bind(listing_id)
    .fetch_all(pool)
    .await?;
    Ok(rows.iter().map(|r| r.get("source_url")).collect())
}

/// Mark an image as cached by filling in sha256, phash, and ext.
pub async fn update_cached_image(
    pool: &SqlitePool,
    listing_id: i64,
    source_url: &str,
    sha256: &str,
    phash: i64,
    ext: &str,
) -> Result<(), sqlx::Error> {
    sqlx::query(
        "UPDATE images_cache SET sha256 = ?, phash = ?, ext = ?
         WHERE listing_id = ? AND source_url = ?",
    )
    .bind(sha256)
    .bind(phash)
    .bind(ext)
    .bind(listing_id)
    .bind(source_url)
    .execute(pool)
    .await?;
    Ok(())
}

/// Resolved images for a listing with metadata: serve URL if cached, source_url as fallback.
pub async fn list_images_with_meta(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<Vec<ImageEntry>, sqlx::Error> {
    let rows = sqlx::query(
        "SELECT id, sha256, ext, source_url, created_at
         FROM images_cache WHERE listing_id = ? ORDER BY position",
    )
    .bind(listing_id)
    .fetch_all(pool)
    .await?;
    Ok(rows
        .iter()
        .map(|r| {
            let ext: Option<String> = r.get("ext");
            let url = match ext {
                Some(ref e) => paths::serve_url(listing_id, &r.get::<String, _>("sha256"), e),
                None => r.get("source_url"),
            };
            ImageEntry {
                id: r.get("id"),
                url,
                created_at: r.get("created_at"),
            }
        })
        .collect())
}

/// Returns the (sha256, ext) for an image, or None if not yet downloaded / row not found.
/// The outer Option is None when the row doesn't exist for this listing.
pub async fn get_image_ext(
    pool: &SqlitePool,
    image_id: i64,
    listing_id: i64,
) -> Result<Option<Option<(String, String)>>, sqlx::Error> {
    let row = sqlx::query("SELECT sha256, ext FROM images_cache WHERE id = ? AND listing_id = ?")
        .bind(image_id)
        .bind(listing_id)
        .fetch_optional(pool)
        .await?;
    Ok(row.map(|r| {
        let ext: Option<String> = r.get("ext");
        ext.map(|e| (r.get("sha256"), e))
    }))
}

/// Delete all images_cache rows for a listing.
/// Call after all image files have been removed from the object store.
pub async fn delete_all_image_records(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<(), sqlx::Error> {
    sqlx::query("DELETE FROM images_cache WHERE listing_id = ?")
        .bind(listing_id)
        .execute(pool)
        .await?;
    Ok(())
}

/// Delete an image_cache row. Call after removing any file from the object store.
pub async fn delete_image_record(
    pool: &SqlitePool,
    image_id: i64,
    listing_id: i64,
) -> Result<(), sqlx::Error> {
    sqlx::query("DELETE FROM images_cache WHERE id = ? AND listing_id = ?")
        .bind(image_id)
        .bind(listing_id)
        .execute(pool)
        .await?;
    Ok(())
}
