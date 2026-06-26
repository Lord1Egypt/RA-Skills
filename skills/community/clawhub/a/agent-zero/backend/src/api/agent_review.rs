//! POST /api/listings/:id/agent-review
//!
//! Called by the background agent task (or the skill in standalone mode) to
//! apply the result of an AI triage decision:
//!
//!   - `HumanReview` + `search_profile_id` — listing matched a profile; ready for human review.
//!   - `AgentSkip`                           — no profile matched; listing is deprioritised.
//!
//! In both cases `agent_comment` is stored so the human can see the reasoning.

use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use serde::Deserialize;

use crate::models::property::{ListingStatus, Property};
use crate::store::{image_store, open_house_store, property_store, search_profile_store};
use crate::AppState;

/// POST /api/listings/:id/agent-review/run
///
/// Re-triggers the background agent review for an existing listing.
/// Returns 202 Accepted immediately; the review runs asynchronously.
pub(crate) async fn trigger_agent_review(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<StatusCode, (StatusCode, String)> {
    let stored = property_store::fetch_stored_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {e}")))?;

    let db = state.db.clone();
    let client = state.client.clone();
    tokio::spawn(async move {
        crate::agent::review::run_agent_review(id, stored, db, client).await;
    });

    Ok(StatusCode::ACCEPTED)
}

#[derive(Deserialize)]
pub struct AgentReviewRequest {
    /// Must be `HumanReview` or `AgentSkip`.
    pub status: ListingStatus,
    /// Required when `status` is `HumanReview`; ignored for `AgentSkip`.
    pub search_profile_id: Option<i64>,
    /// One-sentence reason for the decision.
    pub comment: String,
}

/// POST /api/listings/:id/agent-review
pub(crate) async fn post_agent_review(
    State(state): State<AppState>,
    Path(id): Path<i64>,
    Json(body): Json<AgentReviewRequest>,
) -> Result<Json<Property>, (StatusCode, String)> {
    // Validate the requested status transition.
    match body.status {
        ListingStatus::HumanReview | ListingStatus::AgentSkip => {}
        other => {
            return Err((
                StatusCode::BAD_REQUEST,
                format!(
                    "Invalid agent-review status '{other}'. Must be 'HumanReview' or 'AgentSkip'."
                ),
            ));
        }
    }

    // HumanReview requires a valid search profile.
    if body.status == ListingStatus::HumanReview {
        let profile_id = body.search_profile_id.ok_or((
            StatusCode::BAD_REQUEST,
            "search_profile_id is required when status is HumanReview".to_string(),
        ))?;
        search_profile_store::get_by_id(&state.db, profile_id)
            .await
            .map_err(|e| match e {
                sqlx::Error::RowNotFound => (
                    StatusCode::BAD_REQUEST,
                    format!("search_profile_id {profile_id} does not exist"),
                ),
                _ => (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")),
            })?;
    }

    // Load current listing to confirm it exists.
    property_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("Listing not found: {e}")))?;

    // Apply the decision atomically.
    sqlx::query(
        "UPDATE listings
         SET status = ?, search_profile_id = ?, agent_comment = ?, updated_at = datetime('now')
         WHERE id = ?",
    )
    .bind(body.status)
    .bind(body.search_profile_id)
    .bind(&body.comment)
    .bind(id)
    .execute(&state.db)
    .await
    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;

    tracing::info!(
        "agent_review: id={} → {:?} profile={:?} comment={:?}",
        id,
        body.status,
        body.search_profile_id,
        body.comment,
    );

    // Return the updated property.
    let saved = property_store::fetch_stored_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    let images = image_store::list_images_with_meta(&state.db, id)
        .await
        .unwrap_or_default();
    let open_houses = open_house_store::list_open_houses(&state.db, id)
        .await
        .unwrap_or_default();

    Ok(Json(Property::from_stored(saved, images, open_houses)))
}
