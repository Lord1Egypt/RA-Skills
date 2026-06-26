use crate::images::paths;
use crate::models::image::CachedImage;
use crate::store::image_store;
use image::imageops::FilterType;
use object_store::{path::Path as ObjectPath, ObjectStore, ObjectStoreExt};
use reqwest::Client;
use sha2::{Digest, Sha256};
use sqlx::SqlitePool;
use tokio::fs;

/// Maximum Hamming distance between two dHashes to be considered duplicates.
const PHASH_THRESHOLD: u32 = 8;

/// Compute a 64-bit difference hash (dHash) for perceptual deduplication.
/// Resize to 9×8 grayscale, compare adjacent pixels in each row.
fn dhash(img: &image::DynamicImage) -> i64 {
    let small = img.resize_exact(9, 8, FilterType::Lanczos3).grayscale();
    let pixels = small.to_luma8().into_raw();
    let mut hash: u64 = 0;
    for row in 0..8u32 {
        for col in 0..8u32 {
            let left = pixels[(row * 9 + col) as usize];
            let right = pixels[(row * 9 + col + 1) as usize];
            hash = (hash << 1) | if left > right { 1 } else { 0 };
        }
    }
    hash as i64
}

fn hamming(a: i64, b: i64) -> u32 {
    (a ^ b).count_ones()
}

/// Detect image format from bytes and return file extension.
fn image_ext(bytes: &[u8]) -> &'static str {
    match image::guess_format(bytes) {
        Ok(image::ImageFormat::Jpeg) => "jpg",
        Ok(image::ImageFormat::Png) => "png",
        Ok(image::ImageFormat::WebP) => "webp",
        _ => "jpg",
    }
}

/// Download and cache all pending images for a listing.
///
/// "Pending" means rows in images_cache where ext IS NULL.
/// On success, sha256 / phash / ext are written back to the row.
/// On failure (404, network error, decode error), the row is left with
/// NULL fields so the API falls back to source_url.
///
/// Returns the number of images newly written to the store.
pub async fn cache_images(
    pool: &SqlitePool,
    client: &Client,
    store: &dyn ObjectStore,
    listing_id: i64,
) -> usize {
    // Already-cached images for this listing (for SHA-256 / dHash dedup).
    let mut cached = image_store::list_cached_images(pool, listing_id)
        .await
        .unwrap_or_default();

    // URLs registered but not yet downloaded.
    let pending = match image_store::list_pending_image_urls(pool, listing_id).await {
        Ok(urls) => urls,
        Err(e) => {
            tracing::error!(
                "Failed to list pending images for listing {}: {}",
                listing_id,
                e
            );
            return 0;
        }
    };

    tracing::info!(
        "cache_images: listing_id={} pending={} already_cached= {}",
        listing_id,
        pending.len(),
        cached.len()
    );

    if pending.is_empty() {
        return 0;
    }

    let mut newly_cached = 0usize;

    for url in &pending {
        // Download image bytes.
        let bytes = match client.get(url).send().await {
            Ok(resp) => match resp.error_for_status() {
                Ok(resp) => match resp.bytes().await {
                    Ok(b) => b,
                    Err(e) => {
                        tracing::warn!("Failed to read image bytes {}: {}", url, e);
                        continue;
                    }
                },
                Err(e) => {
                    tracing::warn!("Image URL returned error status {}: {}", url, e);
                    continue;
                }
            },
            Err(e) => {
                tracing::warn!("Failed to download image {}: {}", url, e);
                continue;
            }
        };

        // SHA-256 — exact duplicate within this listing.
        let sha256 = hex::encode(Sha256::digest(&bytes));
        if let Some(c) = cached.iter().find(|c| c.sha256 == sha256) {
            let _ = image_store::update_cached_image(pool, listing_id, url, &sha256, c.phash, &c.ext).await;
            continue;
        }

        // Decode image for dHash.
        let ph = match image::load_from_memory(&bytes) {
            Ok(img) => dhash(&img),
            Err(e) => {
                tracing::warn!("Could not decode image {}: {}", url, e);
                // Store the file anyway; skip dHash dedup.
                0i64
            }
        };

        // dHash dedup — perceptual duplicate within this listing (only when ph != 0).
        if ph != 0 {
            if let Some(existing) = cached
                .iter()
                .find(|c| hamming(c.phash, ph) <= PHASH_THRESHOLD)
            {
                tracing::debug!(
                    "dHash duplicate for {} (distance={})",
                    url,
                    hamming(existing.phash, ph)
                );
                let _ = image_store::update_cached_image(pool, listing_id, url, &sha256, ph, &existing.ext)
                    .await;
                continue;
            }
        }

        // Write to object store.
        let ext = image_ext(&bytes);
        let object_key = ObjectPath::from(paths::object_key(listing_id, &sha256, ext));

        if let Err(e) = store.put(&object_key, bytes.clone().into()).await {
            tracing::warn!("Failed to write image to store {}: {}", object_key, e);
            continue;
        }

        let _ = image_store::update_cached_image(pool, listing_id, url, &sha256, ph, ext).await;

        // Update in-memory list for subsequent dedup checks.
        cached.push(CachedImage {
            sha256,
            phash: ph,
            ext: ext.to_string(),
        });

        newly_cached += 1;
    }

    newly_cached
}

/// Ensure the local images directory exists at startup.
/// Only needed for LocalFileSystem — cloud stores (S3, GCS) don't require this.
pub async fn ensure_images_dir(path: &std::path::Path) {
    if let Err(e) = fs::create_dir_all(path).await {
        tracing::warn!("Could not create images dir {}: {}", path.display(), e);
    }
}
