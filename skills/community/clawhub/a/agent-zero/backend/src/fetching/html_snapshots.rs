//! Persist raw listing HTML to disk for offline inspection and parser backfills.
//!
//! Files are written to `{data_root}/html_snapshots/` as:
//!   `{listing_id}_{source}.html`
//! e.g. `42_redfin.html`, `42_rew.html`
//!
//! On refresh the file is overwritten with the latest fetch so it always
//! reflects the most recent page seen by the backend.

use std::path::{Path, PathBuf};
use tokio::fs;

/// Returns the snapshots directory path derived from the global data root.
pub fn dir() -> PathBuf {
    crate::data_root().join("html_snapshots")
}

/// Create the snapshots directory if it doesn't exist.
pub async fn ensure_dir(dir: &Path) {
    if let Err(e) = fs::create_dir_all(dir).await {
        tracing::warn!("html_snapshots: could not create directory '{}': {}", dir.display(), e);
    }
}

/// Write `html` to `{dir()}/{listing_id}_{source}.html`.
/// Silently skips empty HTML (e.g. blocked-host stubs).
pub(crate) async fn save_listing_html(listing_id: i64, site: crate::parsers::ListingSite, html: &str) {
    if html.is_empty() {
        return;
    }
    let label = site.name();
    let path = dir().join(format!("{listing_id}_{label}.html"));
    match fs::write(&path, html.as_bytes()).await {
        Ok(_) => tracing::debug!(
            "html_snapshots: saved {} bytes → {}",
            html.len(),
            path.display()
        ),
        Err(e) => tracing::warn!("html_snapshots: failed to write {}: {}", path.display(), e),
    }
}
