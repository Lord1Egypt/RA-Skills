//! Models module - contains data structures for the application
//!
//! Submodules:
//! - `image`: Image and ImageEntry struct definitions
//! - `property`: Property and UserDetails struct definitions

pub mod history;
pub mod image;
pub mod open_house;
pub mod property;
pub mod search_profile;

pub use history::HistoryEntry;
pub use image::{CachedImage, ImageEntry};
pub use open_house::{OpenHouse, OpenHouseEvent};
pub use property::{Property, StoredProperty, UserDetails};
pub use search_profile::SearchProfile;
