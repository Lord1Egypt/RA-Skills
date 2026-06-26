pub mod agent;
pub mod api;
pub mod cli;
mod finance;
pub mod fetching;
pub mod images;
pub mod models;
pub mod parsers;
pub mod store;

use axum::{
	routing::{delete, get, patch, post, put},
	Router,
};
use object_store::local::LocalFileSystem;
use reqwest::Client;
use crate::store::property_store;
use std::path::{Path, PathBuf};
use std::sync::{Arc, OnceLock};
use std::time::Duration;
use tower_http::cors::{Any, CorsLayer};
use tower_http::services::ServeDir;

/// URL prefix under which cached images are served (must match the `nest_service` mount point).
/// Used by `image_paths::serve_url` to construct the serve URL, e.g. `/images/1/abc.jpg`.
pub const IMAGES_URL_PREFIX: &str = "/images";

/// Resolved data root directory, set once at startup by `build_app()`.
/// All persistent data (DB, images, snapshots) lives under this path.
static DATA_ROOT: OnceLock<PathBuf> = OnceLock::new();

/// Returns the resolved data root directory (e.g. `~/.agent_zero` or the override).
/// Panics if called before `build_app()` initialises it.
pub fn data_root() -> &'static Path {
	DATA_ROOT.get().expect("data_root not initialized")
}

/// Filesystem directory where downloaded images are stored.
pub fn images_local_dir() -> PathBuf {
	data_root().join("listings_images")
}

#[derive(Clone)]
pub(crate) struct AppState {
	pub(crate) db: sqlx::SqlitePool,
	pub(crate) client: Client,
	pub(crate) store: Arc<dyn object_store::ObjectStore>,
}

/// Resolve the data root from `AGENT_ZERO_DATA_DIR` (or default to `~/.agent_zero`),
/// expanding a leading `~` to the user's home directory.
fn resolve_data_root() -> PathBuf {
	let raw = std::env::var("AGENT_ZERO_DATA_DIR")
		.expect("AGENT_ZERO_DATA_DIR environment variable must be set");
	if raw.starts_with('~') {
		let home = dirs::home_dir().expect("Cannot determine home directory");
		home.join(raw.trim_start_matches('~').trim_start_matches('/'))
	} else {
		PathBuf::from(raw)
	}
}

pub async fn build_app() -> Router {
	// Resolve and register data root.
	let data_root = resolve_data_root();
	DATA_ROOT.set(data_root.clone()).expect("build_app called twice");
	eprintln!("data root: {}", data_root.display());

	// Derive paths for DB, images, and snapshots.
	let img_dir = data_root.join("listings_images");
	let snap_dir = data_root.join("html_snapshots");
	let db_file  = data_root.join("listings.db");

	let database_url = std::env::var("DATABASE_URL")
		.unwrap_or_else(|_| format!("sqlite://{}", db_file.display()));

	// Ensure data root exists.
	std::fs::create_dir_all(&data_root).expect("Failed to create data root directory");

	let db = property_store::init(&database_url).await;

	images::ensure_images_dir(&img_dir).await;
	fetching::html_snapshots::ensure_dir(&snap_dir).await;
	let store: Arc<dyn object_store::ObjectStore> = Arc::new(
		LocalFileSystem::new_with_prefix(&img_dir)
			.expect("Failed to initialize local image store"),
	);

	let client = Client::builder()
		.timeout(Duration::from_secs(15))
		.build()
		.unwrap();

	let state = AppState { db, client, store };

	let cors = CorsLayer::new()
		.allow_origin(
			"http://localhost:5173"
				.parse::<axum::http::HeaderValue>()
				.unwrap(),
		)
		.allow_methods(Any)
		.allow_headers(Any);

	Router::new()
		.route("/api/parse", get(api::parse::parse))
		.route(
			"/api/search-profiles",
			post(api::search_profiles::create_search_profile)
				.get(api::search_profiles::list_search_profiles),
		)
		.route(
			"/api/search-profiles/reorder",
			put(api::search_profiles::reorder_search_profiles),
		)
		.route(
			"/api/search-profiles/:id",
			get(api::search_profiles::get_search_profile)
				.patch(api::search_profiles::update_search_profile)
				.delete(api::search_profiles::delete_search_profile),
		)
		.route(
			"/api/listings",
			post(api::add::add_listing).get(api::listings::list_listings),
		)
		.route("/api/listings/agent-suggest", post(api::add::suggest_listing))
		.route("/api/listings/:id", get(api::listings::get_listing))
		.route("/api/listings/:id/delete", delete(api::listings::delete_listing))
		.route("/api/listings/:id/agent-review", post(api::agent_review::post_agent_review))
		.route("/api/listings/:id/agent-review/run", post(api::agent_review::trigger_agent_review))
		.route("/api/listings/:id/refresh", put(api::refresh::refresh_listing))
		.route("/api/listings/:id/preview", get(api::preview::preview_refresh))
		.route("/api/listings/:id/notes", patch(api::details::patch_notes))
		.route("/api/listings/:id/search-profile", patch(api::details::patch_search_profile))
		.route("/api/listings/:id/details", patch(api::details::patch_details))
		.route("/api/listings/:id/history", get(api::details::get_history))
		.route(
			"/api/listings/:id/open-houses",
			get(api::open_houses::get_open_houses),
		)
		.route(
			"/api/listings/:id/open-houses/:oh_id",
			patch(api::open_houses::patch_open_house),
		)
		.route(
			"/api/listings/:id/images/:image_id",
			delete(api::images::delete_image),
		)
		.nest_service(IMAGES_URL_PREFIX, ServeDir::new(images_local_dir()))
		.with_state(state)
		.layer(cors)
}

pub async fn run() {
	tracing_subscriber::fmt::init();
	let app = build_app().await;
	let bind = "127.0.0.1:8000";
	let api_key = std::env::var("ANTHROPIC_API_KEY")
		.expect("ANTHROPIC_API_KEY environment variable must be set");
	let api_key_masked = format!(
		"{}****{}",
		&api_key[..7.min(api_key.len())],
		&api_key[api_key.len().saturating_sub(4)..]
	);
	println!("Starting backend at http://{}", bind);
	println!(
		"  AGENT_ZERO_DATA_DIR = {}",
		std::env::var("AGENT_ZERO_DATA_DIR").as_deref().unwrap_or("(not set)")
	);
	println!(
		"  DATABASE_URL        = {}",
		std::env::var("DATABASE_URL").as_deref().unwrap_or("(derived from data dir)")
	);
	println!(
		"  BACKEND_PORT        = {}",
		std::env::var("BACKEND_PORT").as_deref().unwrap_or("(not set, using 8000)")
	);
	println!("  ANTHROPIC_API_KEY   = {}", api_key_masked);
	let listener = tokio::net::TcpListener::bind(bind).await.unwrap();
	axum::serve(listener, app).await.unwrap();
}
