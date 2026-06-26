use crate::IMAGES_URL_PREFIX;

/// Object-store key for a cached image: `<listing_id>/<sha256>.<ext>`.
/// This is the path relative to the store root used for reads and deletes.
pub fn object_key(listing_id: i64, sha256: &str, ext: &str) -> String {
    format!("{}/{}.{}", listing_id, sha256, ext)
}

/// Serve URL for a cached image: `<IMAGES_URL_PREFIX>/<listing_id>/<sha256>.<ext>`.
/// This is what gets stored in the DB and returned to the frontend.
pub fn serve_url(listing_id: i64, sha256: &str, ext: &str) -> String {
    format!("{}/{}/{}.{}", IMAGES_URL_PREFIX, listing_id, sha256, ext)
}

/// Filesystem path for a listing's image directory: `<images_local_dir>/<listing_id>`.
/// Used to remove the per-listing subdirectory after all images are deleted.
pub fn listing_dir(listing_id: i64) -> std::path::PathBuf {
    crate::images_local_dir().join(listing_id.to_string())
}
