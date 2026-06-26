use serde::{Deserialize, Serialize};
#[cfg(test)]
use ts_rs::TS;

/// A saved search profile / project that groups related property listings.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[cfg_attr(test, derive(TS), ts(export, export_to = "../../frontend/src/bindings/"))]
pub struct SearchProfile {
    pub id: i64,
    pub title: String,
    pub description: String,
    pub position: i64,
    pub created_at: String,
    pub updated_at: Option<String>,
    /// Number of listings belonging to this search profile (populated by queries).
    #[serde(default)]
    pub listing_count: i64,
}
