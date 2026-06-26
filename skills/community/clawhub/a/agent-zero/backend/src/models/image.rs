use serde::{Deserialize, Serialize};
#[cfg(test)]
use ts_rs::TS;

/// A single image entry associated with a property listing.
/// Can be a local cached file or a remote URL.
#[derive(Serialize, Deserialize, Clone)]
#[cfg_attr(test, derive(TS), ts(export, export_to = "../../frontend/src/bindings/"))]
pub struct ImageEntry {
    pub id: i64,
    pub url: String,
    pub created_at: String,
}

/// An image that has been successfully downloaded and cached locally.
/// Only rows with non-null ext are returned here (used for dedup).
pub struct CachedImage {
    pub sha256: String,
    pub phash: i64,
    /// File extension (e.g. `"jpg"`), used to reconstruct the object key and serve URL.
    pub ext: String,
}
