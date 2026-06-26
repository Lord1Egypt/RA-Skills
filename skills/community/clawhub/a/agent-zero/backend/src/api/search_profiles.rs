//! SearchProfile CRUD handlers.
//!
//! - GET    /api/search-profiles         — list all search profiles
//! - POST   /api/search-profiles         — create a new search profile
//! - GET    /api/search-profiles/:id     — get a single search profile
//! - PATCH  /api/search-profiles/:id     — update title / description
//! - DELETE /api/search-profiles/:id     — delete a search profile (detaches listings)

use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use serde::Deserialize;

use crate::models::search_profile::SearchProfile;
use crate::store::search_profile_store;
use crate::AppState;

#[derive(Deserialize)]
pub struct CreateSearchProfileRequest {
    pub title: String,
    #[serde(default)]
    pub description: String,
}

#[derive(Deserialize)]
pub struct UpdateSearchProfileRequest {
    pub title: Option<String>,
    pub description: Option<String>,
}

#[derive(Deserialize)]
pub struct ReorderRequest {
    /// SearchProfile IDs in the desired display order.
    pub ids: Vec<i64>,
}

/// GET /api/search-profiles
pub(crate) async fn list_search_profiles(
    State(state): State<AppState>,
) -> Result<Json<Vec<SearchProfile>>, (StatusCode, String)> {
    let search_profiles = search_profile_store::list_all(&state.db)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    Ok(Json(search_profiles))
}

/// POST /api/search-profiles
pub(crate) async fn create_search_profile(
    State(state): State<AppState>,
    Json(body): Json<CreateSearchProfileRequest>,
) -> Result<Json<SearchProfile>, (StatusCode, String)> {
    if body.title.trim().is_empty() {
        return Err((StatusCode::BAD_REQUEST, "title is required".to_string()));
    }
    let search_profile = search_profile_store::create(&state.db, body.title.trim(), &body.description)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    Ok(Json(search_profile))
}

/// GET /api/search-profiles/:id
pub(crate) async fn get_search_profile(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<SearchProfile>, (StatusCode, String)> {
    let search_profile = search_profile_store::get_by_id(&state.db, id)
        .await
        .map_err(|e| (StatusCode::NOT_FOUND, format!("SearchProfile not found: {e}")))?;
    Ok(Json(search_profile))
}

/// PATCH /api/search-profiles/:id
pub(crate) async fn update_search_profile(
    State(state): State<AppState>,
    Path(id): Path<i64>,
    Json(body): Json<UpdateSearchProfileRequest>,
) -> Result<Json<SearchProfile>, (StatusCode, String)> {
    let search_profile = search_profile_store::update(
        &state.db,
        id,
        body.title.as_deref(),
        body.description.as_deref(),
    )
    .await
    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    Ok(Json(search_profile))
}

/// PUT /api/search-profiles/reorder
pub(crate) async fn reorder_search_profiles(
    State(state): State<AppState>,
    Json(body): Json<ReorderRequest>,
) -> Result<StatusCode, (StatusCode, String)> {
    if body.ids.is_empty() {
        return Err((StatusCode::BAD_REQUEST, "ids must not be empty".to_string()));
    }
    search_profile_store::reorder(&state.db, &body.ids)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    Ok(StatusCode::NO_CONTENT)
}

/// DELETE /api/search-profiles/:id
pub(crate) async fn delete_search_profile(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<StatusCode, (StatusCode, String)> {
    search_profile_store::delete(&state.db, id)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, format!("DB error: {e}")))?;
    Ok(StatusCode::NO_CONTENT)
}
