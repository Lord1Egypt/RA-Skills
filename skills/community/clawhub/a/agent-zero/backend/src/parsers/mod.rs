//! Parsers for different listing sources.
//!
//! Each parser lives in its own submodule and exposes:
//!   - `parse(url: &str, html: &str) -> Option<ParsedListing>`
//!
//! The top-level `parse()` function dispatches to the right parser based on the URL.

pub mod realtor;
pub mod redfin;
pub mod rew;
pub mod zillow;

#[cfg(test)]
pub(crate) mod test_support;

use crate::models::property::StoredProperty;
use scraper::{Html, Selector};
use serde::Serialize;
use serde_json::Value as JsonValue;
use std::collections::BTreeMap;
use std::fmt::Debug;

// ── Shared output types ───────────────────────────────────────────────────────

pub use crate::models::OpenHouseEvent;

/// The normalised result of parsing a listing page: structured property data,
/// the ordered list of image source URLs, and any open house events.
pub struct ParsedListing {
    pub property: StoredProperty,
    pub image_urls: Vec<String>,
    pub open_houses: Vec<OpenHouseEvent>,
}

/// A (url, html) pair handed to `parse_multi`.
pub struct SourceInput {
    pub url: String,
    pub html: String,
}

/// Raw debug output returned by `GET /api/parse`.
#[derive(Serialize)]
pub struct ParseResult {
    pub url: String,
    pub title: String,
    pub description: String,
    pub images: Vec<String>,
    pub raw_json_ld: Vec<JsonValue>,
    pub meta: BTreeMap<String, String>,
}

// ── Generic HTML utilities (shared across parsers) ────────────────────────────

pub fn extract_json_ld(document: &Html) -> Vec<JsonValue> {
    let selector = Selector::parse("script[type=\"application/ld+json\"]").unwrap();
    let mut out = Vec::new();
    for el in document.select(&selector) {
        if let Some(text) = el.first_child().and_then(|n| n.value().as_text()) {
            let s = text.trim();
            if s.is_empty() {
                continue;
            }
            if let Ok(v) = serde_json::from_str::<JsonValue>(s) {
                if v.is_array() {
                    if let Some(arr) = v.as_array() {
                        for item in arr {
                            out.push(item.clone());
                        }
                    }
                } else {
                    out.push(v);
                }
            }
        }
    }
    out
}

pub fn meta_map(document: &Html) -> BTreeMap<String, String> {
    let mut m = BTreeMap::new();
    let selector = Selector::parse("meta").unwrap();
    for el in document.select(&selector) {
        let name = el
            .value()
            .attr("property")
            .or_else(|| el.value().attr("name"))
            .unwrap_or("");
        if name.is_empty() {
            continue;
        }
        if let Some(content) = el.value().attr("content") {
            m.insert(name.to_string(), content.to_string());
        }
    }
    m
}

pub fn extract_title(document: &Html) -> String {
    let og = Selector::parse("meta[property=\"og:title\"]").unwrap();
    if let Some(el) = document.select(&og).next() {
        if let Some(content) = el.value().attr("content") {
            return content.to_string();
        }
    }
    let title = Selector::parse("title").unwrap();
    if let Some(el) = document.select(&title).next() {
        return el.text().collect::<Vec<_>>().join("").trim().to_string();
    }
    String::new()
}

pub fn extract_description(document: &Html) -> String {
    let sel =
        Selector::parse("meta[property=\"og:description\"], meta[name=\"description\"]").unwrap();
    if let Some(el) = document.select(&sel).next() {
        if let Some(content) = el.value().attr("content") {
            return content.to_string();
        }
    }
    String::new()
}

pub fn extract_images(document: &Html) -> Vec<String> {
    let sel = Selector::parse("meta[property=\"og:image\"]").unwrap();
    let mut out = Vec::new();
    for el in document.select(&sel) {
        if let Some(content) = el.value().attr("content") {
            out.push(content.to_string());
        }
    }
    out
}

// ── Parser dispatch ───────────────────────────────────────────────────────────

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum ListingSite {
    Redfin,
    Rew,
    Zillow,
    Realtor,
}

impl ListingSite {
    pub(crate) fn name(self) -> &'static str {
        match self {
            ListingSite::Redfin => "redfin",
            ListingSite::Rew => "rew",
            ListingSite::Zillow => "zillow",
            ListingSite::Realtor => "realtor",
        }
    }

    pub(crate) fn from_url(url: &str) -> Option<Self> {
        if url.contains("redfin.") {
            Some(ListingSite::Redfin)
        } else if url.contains("rew.ca") {
            Some(ListingSite::Rew)
        } else if url.contains("zillow.com") {
            Some(ListingSite::Zillow)
        } else if url.contains("realtor.ca") {
            Some(ListingSite::Realtor)
        } else {
            None
        }
    }
}

fn source_rank(site: ListingSite) -> u8 {
    match site {
        ListingSite::Redfin => 0,
        ListingSite::Rew => 1,
        ListingSite::Zillow => 2,
        ListingSite::Realtor => 3,
    }
}

/// A successfully parsed listing tagged with the source that produced it.
struct ParsedSource {
    site: ListingSite,
    listing: ParsedListing,
}

fn merge_opt<T>(
    field: &str,
    primary: Option<T>,
    fallback: Option<T>,
    primary_source: ListingSite,
    fallback_source: ListingSite,
) -> Option<T>
where
    T: PartialEq + Clone + Debug,
{
    match (primary, fallback) {
        (Some(p), Some(f)) if p != f => {
            tracing::warn!(
                "merge conflict on {}: {}={:?} {}={:?} — keeping {}",
                field,
                primary_source.name(),
                p,
                fallback_source.name(),
                f,
                primary_source.name(),
            );
            Some(p)
        }
        (Some(p), _) => Some(p),
        (None, fallback) => fallback,
    }
}

fn merge_text(primary: String, fallback: String) -> String {
    if primary.trim().is_empty() {
        fallback
    } else {
        primary
    }
}

fn merge_property(
    primary: StoredProperty,
    fallback: StoredProperty,
    primary_source: ListingSite,
    fallback_source: ListingSite,
) -> StoredProperty {
    StoredProperty {
        id: primary.id,
        search_profile_id: primary.search_profile_id,

        redfin_url: primary.redfin_url.or(fallback.redfin_url),
        realtor_url: primary.realtor_url.or(fallback.realtor_url),
        rew_url: primary.rew_url.or(fallback.rew_url),
        zillow_url: primary.zillow_url.or(fallback.zillow_url),

        title: merge_text(primary.title, fallback.title),
        description: merge_text(primary.description, fallback.description),

        price: merge_opt(
            "price",
            primary.price,
            fallback.price,
            primary_source,
            fallback_source,
        ),
        price_currency: merge_opt(
            "price_currency",
            primary.price_currency,
            fallback.price_currency,
            primary_source,
            fallback_source,
        ),
        offer_price: merge_opt(
            "offer_price",
            primary.offer_price,
            fallback.offer_price,
            primary_source,
            fallback_source,
        ),

        street_address: merge_opt(
            "street_address",
            primary.street_address,
            fallback.street_address,
            primary_source,
            fallback_source,
        ),
        city: merge_opt(
            "city",
            primary.city,
            fallback.city,
            primary_source,
            fallback_source,
        ),
        region: merge_opt(
            "region",
            primary.region,
            fallback.region,
            primary_source,
            fallback_source,
        ),
        postal_code: merge_opt(
            "postal_code",
            primary.postal_code,
            fallback.postal_code,
            primary_source,
            fallback_source,
        ),
        country: merge_opt(
            "country",
            primary.country,
            fallback.country,
            primary_source,
            fallback_source,
        ),

        bedrooms: merge_opt(
            "bedrooms",
            primary.bedrooms,
            fallback.bedrooms,
            primary_source,
            fallback_source,
        ),
        bathrooms: merge_opt(
            "bathrooms",
            primary.bathrooms,
            fallback.bathrooms,
            primary_source,
            fallback_source,
        ),
        sqft: merge_opt(
            "sqft",
            primary.sqft,
            fallback.sqft,
            primary_source,
            fallback_source,
        ),
        year_built: merge_opt(
            "year_built",
            primary.year_built,
            fallback.year_built,
            primary_source,
            fallback_source,
        ),

        lat: merge_opt(
            "lat",
            primary.lat,
            fallback.lat,
            primary_source,
            fallback_source,
        ),
        lon: merge_opt(
            "lon",
            primary.lon,
            fallback.lon,
            primary_source,
            fallback_source,
        ),

        created_at: merge_text(primary.created_at, fallback.created_at),
        updated_at: merge_opt(
            "updated_at",
            primary.updated_at,
            fallback.updated_at,
            primary_source,
            fallback_source,
        ),
        notes: merge_opt(
            "notes",
            primary.notes,
            fallback.notes,
            primary_source,
            fallback_source,
        ),

        parking_total: merge_opt(
            "parking_total",
            primary.parking_total,
            fallback.parking_total,
            primary_source,
            fallback_source,
        ),

        parking_garage: merge_opt(
            "parking_garage",
            primary.parking_garage,
            fallback.parking_garage,
            primary_source,
            fallback_source,
        ),
        parking_carport: merge_opt(
            "parking_carport",
            primary.parking_carport,
            fallback.parking_carport,
            primary_source,
            fallback_source,
        ),
        parking_pad: merge_opt(
            "parking_pad",
            primary.parking_pad,
            fallback.parking_pad,
            primary_source,
            fallback_source,
        ),
        land_sqft: merge_opt(
            "land_sqft",
            primary.land_sqft,
            fallback.land_sqft,
            primary_source,
            fallback_source,
        ),
        property_tax: merge_opt(
            "property_tax",
            primary.property_tax,
            fallback.property_tax,
            primary_source,
            fallback_source,
        ),

        skytrain_station: merge_opt(
            "skytrain_station",
            primary.skytrain_station,
            fallback.skytrain_station,
            primary_source,
            fallback_source,
        ),
        skytrain_walk_min: merge_opt(
            "skytrain_walk_min",
            primary.skytrain_walk_min,
            fallback.skytrain_walk_min,
            primary_source,
            fallback_source,
        ),

        radiant_floor_heating: merge_opt(
            "radiant_floor_heating",
            primary.radiant_floor_heating,
            fallback.radiant_floor_heating,
            primary_source,
            fallback_source,
        ),
        ac: merge_opt(
            "ac",
            primary.ac,
            fallback.ac,
            primary_source,
            fallback_source,
        ),

        down_payment_pct: merge_opt(
            "down_payment_pct",
            primary.down_payment_pct,
            fallback.down_payment_pct,
            primary_source,
            fallback_source,
        ),
        mortgage_interest_rate: merge_opt(
            "mortgage_interest_rate",
            primary.mortgage_interest_rate,
            fallback.mortgage_interest_rate,
            primary_source,
            fallback_source,
        ),
        amortization_years: merge_opt(
            "amortization_years",
            primary.amortization_years,
            fallback.amortization_years,
            primary_source,
            fallback_source,
        ),
        mortgage_monthly: merge_opt(
            "mortgage_monthly",
            primary.mortgage_monthly,
            fallback.mortgage_monthly,
            primary_source,
            fallback_source,
        ),
        hoa_monthly: merge_opt(
            "hoa_monthly",
            primary.hoa_monthly,
            fallback.hoa_monthly,
            primary_source,
            fallback_source,
        ),
        monthly_total: merge_opt(
            "monthly_total",
            primary.monthly_total,
            fallback.monthly_total,
            primary_source,
            fallback_source,
        ),
        monthly_cost: merge_opt(
            "monthly_cost",
            primary.monthly_cost,
            fallback.monthly_cost,
            primary_source,
            fallback_source,
        ),

        has_rental_suite: merge_opt(
            "has_rental_suite",
            primary.has_rental_suite,
            fallback.has_rental_suite,
            primary_source,
            fallback_source,
        ),
        rental_income: merge_opt(
            "rental_income",
            primary.rental_income,
            fallback.rental_income,
            primary_source,
            fallback_source,
        ),

        status: primary.status,

        school_elementary: merge_opt(
            "school_elementary",
            primary.school_elementary,
            fallback.school_elementary,
            primary_source,
            fallback_source,
        ),
        school_elementary_rating: merge_opt(
            "school_elementary_rating",
            primary.school_elementary_rating,
            fallback.school_elementary_rating,
            primary_source,
            fallback_source,
        ),
        school_middle: merge_opt(
            "school_middle",
            primary.school_middle,
            fallback.school_middle,
            primary_source,
            fallback_source,
        ),
        school_middle_rating: merge_opt(
            "school_middle_rating",
            primary.school_middle_rating,
            fallback.school_middle_rating,
            primary_source,
            fallback_source,
        ),
        school_secondary: merge_opt(
            "school_secondary",
            primary.school_secondary,
            fallback.school_secondary,
            primary_source,
            fallback_source,
        ),
        school_secondary_rating: merge_opt(
            "school_secondary_rating",
            primary.school_secondary_rating,
            fallback.school_secondary_rating,
            primary_source,
            fallback_source,
        ),
        property_type: merge_opt(
            "property_type",
            primary.property_type,
            fallback.property_type,
            primary_source,
            fallback_source,
        ),
        listed_date: merge_opt(
            "listed_date",
            primary.listed_date,
            fallback.listed_date,
            primary_source,
            fallback_source,
        ),
        mls_number: merge_opt(
            "mls_number",
            primary.mls_number,
            fallback.mls_number,
            primary_source,
            fallback_source,
        ),
        laundry_in_unit: merge_opt(
            "laundry_in_unit",
            primary.laundry_in_unit,
            fallback.laundry_in_unit,
            primary_source,
            fallback_source,
        ),
        source_status: None, // cleared by a successful parse
        agent_comment: None,
    }
}

fn merge_listing(
    primary: ParsedListing,
    fallback: ParsedListing,
    primary_source: ListingSite,
    fallback_source: ListingSite,
) -> ParsedListing {
    let mut image_urls = primary.image_urls;
    for image_url in fallback.image_urls {
        if !image_urls.iter().any(|existing| existing == &image_url) {
            image_urls.push(image_url);
        }
    }

    let mut open_houses = primary.open_houses;
    for oh in fallback.open_houses {
        if !open_houses.iter().any(|e| e.start_time == oh.start_time) {
            open_houses.push(oh);
        }
    }

    ParsedListing {
        property: merge_property(
            primary.property,
            fallback.property,
            primary_source,
            fallback_source,
        ),
        image_urls,
        open_houses,
    }
}

fn parse_source(url: &str, html: &str) -> Option<ParsedSource> {
    let site = ListingSite::from_url(url)?;
    let listing = match site {
        ListingSite::Redfin => redfin::parse(url, html)?,
        ListingSite::Rew => rew::parse(url, html)?,
        ListingSite::Zillow => zillow::parse(url, html)?,
        ListingSite::Realtor => realtor::parse(url, html)?,
    };
    Some(ParsedSource { site, listing })
}

/// Parses and merges data from multiple listing pages for the same property.
///
/// Strategy:
/// - Redfin is the primary source for all fields.
/// - Other successful parsers fill in missing fields by priority order.
/// - When two sources disagree on the same populated field, keeps the higher-priority value.
///
/// `sources` is a slice of `SourceInput` items (url + html). Unknown URLs are ignored.
pub fn parse_multi(sources: &[SourceInput]) -> Option<ParsedListing> {
    let mut parsed: Vec<ParsedSource> = sources
        .iter()
        .filter_map(|s| parse_source(&s.url, &s.html))
        .collect();

    if parsed.is_empty() {
        return None;
    }

    parsed.sort_by_key(|ps| source_rank(ps.site));

    let first = parsed.remove(0);
    let (primary_source, mut merged_listing) = (first.site, first.listing);
    for ps in parsed {
        merged_listing = merge_listing(merged_listing, ps.listing, primary_source, ps.site);
    }

    tracing::info!(
        "parse_multi: merged using primary source={}, property_tax={:?}",
        primary_source.name(),
        merged_listing.property.property_tax
    );
    Some(merged_listing)
}
