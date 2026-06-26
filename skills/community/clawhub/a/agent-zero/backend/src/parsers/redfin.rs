//! Redfin-specific listing parser.
//!
//! Redfin embeds structured data in two places:
//!   - JSON-LD (`RealEstateListing`) for core fields and image URLs.
//!   - An escaped JSON blob in a `<script>` tag for lot size and nearby schools.

use regex::Regex;
use scraper::Html;
use serde_json::Value as JsonValue;
use std::sync::OnceLock;

use super::{extract_json_ld, extract_title, OpenHouseEvent, ParsedListing};
use crate::models::property::{SourceStatus, StoredProperty};

// ── Static regexes ────────────────────────────────────────────────────────────

static GARAGE_RE: OnceLock<Regex> = OnceLock::new();
static LOT_SIZE_RE: OnceLock<Regex> = OnceLock::new();
static NEARBY_SCHOOLS_RE: OnceLock<Regex> = OnceLock::new();
static TAX_ANNUAL_RE: OnceLock<Regex> = OnceLock::new();
static HOA_FEE_RE: OnceLock<Regex> = OnceLock::new();
static PARKING_COUNT_RE: OnceLock<Regex> = OnceLock::new();
static CARPORT_SPACES_RE: OnceLock<Regex> = OnceLock::new();
static OH_DATE_RE: OnceLock<Regex> = OnceLock::new();
static OH_TIME_RE: OnceLock<Regex> = OnceLock::new();
static HOME_STATUS_LABEL_RE: OnceLock<Regex> = OnceLock::new();
static XDP_LISTING_STATUS_RE: OnceLock<Regex> = OnceLock::new();

fn garage_re() -> &'static Regex {
    GARAGE_RE.get_or_init(|| Regex::new(r"(?i)(\d+)\s+garage").unwrap())
}

fn parking_count_re() -> &'static Regex {
    PARKING_COUNT_RE.get_or_init(|| Regex::new(r"(\d+)").unwrap())
}

fn carport_spaces_re() -> &'static Regex {
    CARPORT_SPACES_RE.get_or_init(|| Regex::new(r"(?i)Carport\s+Spaces\s*:?\s*(\d+)").unwrap())
}

/// Matches the month+day portion of an oh-date string like "Saturday, Feb 28" or "Feb 28".
fn oh_date_re() -> &'static Regex {
    OH_DATE_RE.get_or_init(|| Regex::new(r"([A-Za-z]{3,})\s+(\d{1,2})\s*$").unwrap())
}

/// Matches a 12-hour time like "2:00pm" or "10:30am".
fn oh_time_re() -> &'static Regex {
    OH_TIME_RE.get_or_init(|| Regex::new(r"(\d{1,2}):(\d{2})\s*(am|pm)").unwrap())
}

fn home_status_label_re() -> &'static Regex {
    HOME_STATUS_LABEL_RE
        .get_or_init(|| Regex::new(r#"\\?"homeStatusLabel\\?":\s*\\?"([^"\\]+)\\?""#).unwrap())
}

/// Matches `"listingStatus": "pending"` inside the `xdp-meta` JSON block.
fn xdp_listing_status_re() -> &'static Regex {
    XDP_LISTING_STATUS_RE.get_or_init(|| {
        Regex::new(r#"id="xdp-meta">\s*\{[^}]*"listingStatus":\s*"([^"]+)""#).unwrap()
    })
}

fn lot_size_re() -> &'static Regex {
    LOT_SIZE_RE.get_or_init(|| Regex::new(r#"lotSize\\?\":(\d+)"#).unwrap())
}

fn nearby_schools_re() -> &'static Regex {
    NEARBY_SCHOOLS_RE.get_or_init(|| Regex::new(r#""nearbySchools":\s*(\[[^\]]*\])"#).unwrap())
}

fn tax_annual_re() -> &'static Regex {
    TAX_ANNUAL_RE.get_or_init(|| Regex::new(r"Tax Annual Amount:\s*\$?([\d,]+)").unwrap())
}

/// Matches HOA / strata / maintenance fee text as it appears in Redfin's
/// property-details section.  Handles all of:
///   "HOA Dues: $543/month"
///   "HOA Fee: $200 per month"
///   "Maintenance Fee: $650"
fn hoa_fee_re() -> &'static Regex {
    HOA_FEE_RE.get_or_init(|| {
        Regex::new(r"(?i)(?:hoa\s*dues|hoa\s*fee|maintenance\s*fee)[s]?\s*:?\s*\$?([\d,]+)")
            .unwrap()
    })
}

// ── Open house extraction ────────────────────────────────────────────────────

fn month_abbrev_num(abbrev: &str) -> Option<u32> {
    match abbrev.to_lowercase().as_str() {
        "jan" | "january"   => Some(1),
        "feb" | "february"  => Some(2),
        "mar" | "march"     => Some(3),
        "apr" | "april"     => Some(4),
        "may"               => Some(5),
        "jun" | "june"      => Some(6),
        "jul" | "july"      => Some(7),
        "aug" | "august"    => Some(8),
        "sep" | "september" => Some(9),
        "oct" | "october"   => Some(10),
        "nov" | "november"  => Some(11),
        "dec" | "december"  => Some(12),
        _ => None,
    }
}

/// Parse a 12-hour time string like "2:00pm" into (hour24, minute).
fn parse_12h_time(s: &str) -> Option<(u32, u32)> {
    let caps = oh_time_re().captures(s)?;
    let mut hour: u32 = caps[1].parse().ok()?;
    let min: u32 = caps[2].parse().ok()?;
    let ampm = &caps[3];
    if ampm == "pm" && hour != 12 {
        hour += 12;
    } else if ampm == "am" && hour == 12 {
        hour = 0;
    }
    Some((hour, min))
}

/// Extract open house events from Redfin's `.OpenHouseCard` DOM components.
///
/// Each card contains:
/// - `.oh-date` → e.g. "Saturday, Feb 28"
/// - `.oh-time` → e.g. "2:00pm - 4:00pm"
///
/// `year` is derived from the listing's `listed_date` (fallback: 2026) so that
/// month/day strings are resolved to the correct calendar year.
pub fn extract_open_houses(document: &Html, year: i32) -> Vec<OpenHouseEvent> {
    let (Ok(card_sel), Ok(date_sel), Ok(time_sel)) = (
        scraper::Selector::parse(".OpenHouseCard"),
        scraper::Selector::parse(".oh-date"),
        scraper::Selector::parse(".oh-time"),
    ) else {
        return vec![];
    };

    let mut events = Vec::new();
    for card in document.select(&card_sel) {
        let date_text: String = card
            .select(&date_sel)
            .next()
            .map(|el| el.text().collect())
            .unwrap_or_default();
        let time_text: String = card
            .select(&time_sel)
            .next()
            .map(|el| el.text().collect())
            .unwrap_or_default();

        // Parse month + day from e.g. "Saturday, Feb 28".
        let caps = match oh_date_re().captures(date_text.trim()) {
            Some(c) => c,
            None => continue,
        };
        let month = match month_abbrev_num(&caps[1]) {
            Some(m) => m,
            None => continue,
        };
        let day: u32 = match caps[2].parse() {
            Ok(d) => d,
            Err(_) => continue,
        };

        // Parse start + optional end from e.g. "2:00pm - 4:00pm".
        let parts: Vec<&str> = time_text.trim().splitn(2, " - ").collect();
        let (start_h, start_m) = match parts.first().and_then(|t| parse_12h_time(t)) {
            Some(t) => t,
            None => continue,
        };
        let end_time = parts
            .get(1)
            .and_then(|t| parse_12h_time(t))
            .map(|(h, m)| format!("{:04}-{:02}-{:02}T{:02}:{:02}:00", year, month, day, h, m));

        events.push(OpenHouseEvent {
            start_time: format!(
                "{:04}-{:02}-{:02}T{:02}:{:02}:00",
                year, month, day, start_h, start_m
            ),
            end_time,
        });
    }
    events
}

// ── School extraction ─────────────────────────────────────────────────────────

/// A single school with its name and optional GreatSchools rating.
pub struct SchoolEntry {
    pub name: String,
    pub rating: Option<f64>,
}

pub struct SchoolInfo {
    pub elementary: Option<SchoolEntry>,
    pub middle: Option<SchoolEntry>,
    pub secondary: Option<SchoolEntry>,
}

/// Extracts nearby school names and GreatSchools ratings from Redfin's embedded JSON.
/// Redfin categorises schools as "e" (elementary), "m" (middle), "h" (high/secondary).
/// Returns `None` if no school data is found in the page.
pub fn extract_schools(html: &str) -> Option<SchoolInfo> {
    let caps = nearby_schools_re().captures(html)?;
    let json_str = caps.get(1)?.as_str();
    let schools: JsonValue = serde_json::from_str(json_str).ok()?;
    let arr = schools.as_array()?;

    let mut elementary: Option<SchoolEntry> = None;
    let mut middle: Option<SchoolEntry> = None;
    let mut secondary: Option<SchoolEntry> = None;

    for s in arr {
        let name = match s["name"].as_str().or_else(|| s["schoolName"].as_str()) {
            Some(n) => n.to_string(),
            None => continue,
        };
        let rating = s["rating"]
            .as_f64()
            .or_else(|| s["greatSchoolsRating"].as_f64())
            .or_else(|| s["score"].as_f64());
        let level = s["levelCode"]
            .as_str()
            .or_else(|| s["type"].as_str())
            .or_else(|| s["gradeRange"].as_str())
            .unwrap_or("");

        let lower = level.to_lowercase();
        if (lower.contains('e')
            || lower.starts_with('k')
            || lower.contains("elementary")
            || lower.contains("primary"))
            && elementary.is_none()
        {
            elementary = Some(SchoolEntry { name, rating });
        } else if (lower.contains('m') || lower.contains("middle") || lower.contains("junior"))
            && middle.is_none()
        {
            middle = Some(SchoolEntry { name, rating });
        } else if (lower.contains('h') || lower.contains("high") || lower.contains("secondary"))
            && secondary.is_none()
        {
            secondary = Some(SchoolEntry { name, rating });
        }
    }

    if elementary.is_none() && middle.is_none() && secondary.is_none() {
        return None;
    }

    Some(SchoolInfo {
        elementary,
        middle,
        secondary,
    })
}

// ── Property tax ──────────────────────────────────────────────────────────────

/// Extracts annual property tax from Redfin's property details section.
/// Matches "Tax Annual Amount: $9,082.04" in the rendered HTML.
pub fn extract_property_tax(html: &str) -> Option<i64> {
    let caps = tax_annual_re().captures(html)?;
    let digits: String = caps
        .get(1)?
        .as_str()
        .chars()
        .filter(|c| c.is_ascii_digit())
        .collect();
    digits.parse().ok()
}

// ── HOA / strata fee ──────────────────────────────────────────────────────────

/// Extracts monthly HOA / strata / maintenance fee from Redfin's property
/// details section.
///
/// Redfin surfaces the fee as plain text in two ways:
///
/// 1. In the property-details text block, e.g.:
///    `"HOA Dues: $543/month"` or `"Maintenance Fee: $650"`
///
/// 2. In the escaped JSON blob embedded in a `<script>` tag, e.g.:
///    `"hoaFee":543` or `"maintenanceFee":543`
///
/// Both are tried; the text-block match takes precedence.
pub fn extract_hoa_monthly(html: &str) -> Option<i64> {
    // 1. Text-block match ("HOA Dues: $543/month", "Maintenance Fee: $650", …)
    if let Some(caps) = hoa_fee_re().captures(html) {
        let digits: String = caps
            .get(1)?
            .as_str()
            .chars()
            .filter(|c| c.is_ascii_digit())
            .collect();
        if let Ok(v) = digits.parse::<i64>() {
            if v > 0 {
                return Some(v);
            }
        }
    }
    // 2. Embedded JSON blob — Redfin uses several key names.
    //    The blob is an escaped JSON string, so quotes appear as \" and
    //    the pattern looks like: \"monthlyHoaDues\":1137
    //    Regex: optional-\ + " + key + optional-\ + " + :digits
    let json_re =
        Regex::new(r#"\\?"(?:hoaFee|maintenanceFee|monthlyHoaDues)\\?":\s*(\d+)"#).unwrap();
    if let Some(caps) = json_re.captures(html) {
        if let Ok(v) = caps[1].parse::<i64>() {
            if v > 0 {
                return Some(v);
            }
        }
    }
    None
}

/// Extracts carport spaces from Redfin property details text.
/// Example: "Carport Spaces: 1"
pub fn extract_carport_spaces(html: &str) -> Option<i64> {
    carport_spaces_re()
        .captures(html)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<i64>().ok())
}

// ── Lot size ──────────────────────────────────────────────────────────────────

/// Extracts lot size (sqft) from the raw HTML source.
/// Redfin embeds `"lotSize":3480` as escaped JSON in a script block.
pub fn extract_lot_size(html: &str) -> Option<i64> {
    lot_size_re()
        .captures(html)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse::<i64>().ok())
}

// ── Source status ─────────────────────────────────────────────────────────────

/// Extracts the listing status label from Redfin's HTML.
///
/// Two sources are tried in order:
/// 1. `homeStatusLabel` in the escaped JSON blob (present on off-market/sold pages).
/// 2. `listingStatus` in the `xdp-meta` JSON script tag (present on active/pending pages).
///
/// Returns `None` for "active" listings — active is the normal state and needs no annotation.
pub fn extract_source_status(html: &str) -> Option<SourceStatus> {
    // 1. Escaped JSON blob — authoritative for off-market / sold pages.
    if let Some(caps) = home_status_label_re().captures(html) {
        if let Some(m) = caps.get(1) {
            return Some(m.as_str().parse().unwrap()); // Infallible
        }
    }
    // 2. xdp-meta JSON tag — present on active/pending pages when the blob is absent.
    //    Redfin uses lowercase values like "pending", "active", "sold".
    if let Some(caps) = xdp_listing_status_re().captures(html) {
        if let Some(m) = caps.get(1) {
            let raw = m.as_str();
            // "active" is the normal for-sale state; leave source_status unset.
            if raw.eq_ignore_ascii_case("active") {
                return None;
            }
            return Some(raw.parse().unwrap()); // Infallible
        }
    }
    None
}

// ── Amenity features ──────────────────────────────────────────────────────────

/// Parsed results from a property's `amenityFeature` array.
struct AmenityFeatures {
    parking_total: Option<i64>,
    parking_garage: Option<i64>,
    parking_carport: Option<i64>,
    parking_pad: Option<i64>,
    ac: Option<bool>,
    radiant_floor_heating: Option<bool>,
    laundry_in_unit: Option<bool>,
}

/// Parses `amenityFeature` array entries for parking count, AC, radiant floor heating,
/// and in-unit laundry.
fn parse_amenity_features(features: &[JsonValue]) -> AmenityFeatures {
    let mut parking_total: Option<i64> = None;
    let mut parking_garage: Option<i64> = None;
    let mut parking_carport: Option<i64> = None;
    let mut parking_pad: Option<i64> = None;
    let mut ac: Option<bool> = None;
    let mut radiant_floor_heating: Option<bool> = None;
    let mut laundry_in_unit: Option<bool> = None;

    for f in features {
        let name = match f["name"].as_str() {
            Some(n) => n,
            None => continue,
        };
        let active = f["value"].as_bool().unwrap_or(false);
        let lower = name.to_lowercase();

        if lower.contains("parking") {
            // Handles both "Parking: 2 spaces" and "2 garage spaces" formats.
            let caps = garage_re()
                .captures(name)
                .or_else(|| parking_count_re().captures(name));
            if let Some(n) = caps
                .and_then(|c| c.get(1))
                .and_then(|m| m.as_str().parse::<i64>().ok())
            {
                if lower.contains("garage") {
                    parking_garage = Some(n);
                    parking_total = Some(n);
                } else if lower.contains("carport") || lower.contains("covered") {
                    parking_carport = Some(n);
                    parking_total = Some(n);
                } else if lower.contains("open")
                    || lower.contains("pad")
                    || lower.contains("driveway")
                {
                    parking_pad = Some(n);
                    parking_total = Some(n);
                } else {
                    parking_total = Some(n);
                }
            }
        } else if active && lower.contains("laundry") {
            laundry_in_unit = Some(true);
        } else if active && (lower.contains("air conditioning") || lower.contains(" a/c")) {
            ac = Some(true);
        } else if active && lower.contains("radiant") {
            radiant_floor_heating = Some(true);
        }
    }

    AmenityFeatures {
        parking_total,
        parking_garage,
        parking_carport,
        parking_pad,
        ac,
        radiant_floor_heating,
        laundry_in_unit,
    }
}

// ── JSON-LD extraction ────────────────────────────────────────────────────────

/// Extracts structured property fields from JSON-LD blocks.
/// Looks for the item whose `@type` includes `"RealEstateListing"`.
/// `images` is always left empty — `extract_image_urls` handles that.
pub fn extract_property(url: &str, title: &str, json_ld: &[JsonValue]) -> Option<StoredProperty> {
    let listing = json_ld.iter().find(|v| {
        let t = &v["@type"];
        t == "RealEstateListing"
            || t.as_array()
                .map(|a| a.iter().any(|x| x == "RealEstateListing"))
                .unwrap_or(false)
    })?;

    let entity = &listing["mainEntity"];
    let addr = &entity["address"];

    let description = listing["description"].as_str().unwrap_or("").to_string();
    let price = listing["offers"]["price"].as_i64();
    // Redfin embeds "priceCurrency":"USD" even for non-US listings — a known
    // data bug on their side. Derive the correct currency from addressCountry
    // instead: "CA" → CAD, "US" → USD, anything else falls back to the field.
    let price_currency = match addr["addressCountry"].as_str() {
        Some("CA") => Some("CAD".to_string()),
        Some("US") => Some("USD".to_string()),
        _ => listing["offers"]["priceCurrency"].as_str().map(str::to_string),
    };
    let street_address = addr["streetAddress"].as_str().map(str::to_string);
    let city = addr["addressLocality"].as_str().map(str::to_string);
    let region = addr["addressRegion"].as_str().map(str::to_string);
    let postal_code = addr["postalCode"].as_str().map(str::to_string);
    let country = addr["addressCountry"].as_str().map(str::to_string);
    let bedrooms = entity["numberOfBedrooms"].as_i64();
    let bathrooms = entity["numberOfBathroomsTotal"].as_i64();
    let sqft = entity["floorSize"]["value"].as_i64();
    let year_built = entity["yearBuilt"].as_i64();
    let lat = entity["geo"]["latitude"].as_f64();
    let lon = entity["geo"]["longitude"].as_f64();

    let amenities = entity["amenityFeature"]
        .as_array()
        .map(Vec::as_slice)
        .unwrap_or(&[]);
    let af = parse_amenity_features(amenities);

    let property_type = entity["accommodationCategory"].as_str().map(str::to_string);
    let listed_date = listing["datePosted"]
        .as_str()
        .map(|s| s[..s.len().min(10)].to_string());

    Some(StoredProperty {
        id: 0,
        search_profile_id: None, // overwritten by caller
        redfin_url: Some(url.to_string()),
        realtor_url: None,
        rew_url: None,
        zillow_url: None,
        title: title.to_string(),
        description,
        price,
        price_currency,
        offer_price: None,
        street_address,
        city,
        region,
        postal_code,
        country,
        bedrooms,
        bathrooms,
        sqft,
        year_built,
        lat,
        lon,
        created_at: String::new(),
        updated_at: None,
        notes: None,
        parking_total: af.parking_total,
        parking_garage: af.parking_garage,
        parking_carport: af.parking_carport,
        parking_pad: af.parking_pad,
        land_sqft: None,
        property_tax: None,
        skytrain_station: None,
        skytrain_walk_min: None,
        radiant_floor_heating: af.radiant_floor_heating,
        ac: af.ac,
        laundry_in_unit: af.laundry_in_unit,
        source_status: None,
        agent_comment: None,
        // Mortgage params are set by main.rs after parsing (save/refresh handlers).
        down_payment_pct: None,
        mortgage_interest_rate: None,
        amortization_years: None,
        mortgage_monthly: None,
        hoa_monthly: None,
        monthly_total: None,
        monthly_cost: None,
        has_rental_suite: None,
        rental_income: None,
        status: crate::models::property::ListingStatus::Interested,
        school_elementary: None,
        school_elementary_rating: None,
        school_middle: None,
        school_middle_rating: None,
        school_secondary: None,
        school_secondary_rating: None,
        property_type,
        listed_date,
        mls_number: None,
    })
}

/// Extracts image source URLs from `mainEntity.image[]` in the JSON-LD block.
pub fn extract_image_urls(json_ld: &[JsonValue]) -> Vec<String> {
    let listing = json_ld.iter().find(|v| {
        let t = &v["@type"];
        t == "RealEstateListing"
            || t.as_array()
                .map(|a| a.iter().any(|x| x == "RealEstateListing"))
                .unwrap_or(false)
    });
    listing
        .and_then(|l| l["mainEntity"]["image"].as_array())
        .map(|imgs| {
            imgs.iter()
                .filter_map(|img| img["url"].as_str().map(str::to_string))
                .collect()
        })
        .unwrap_or_default()
}

// ── MLS number extraction ────────────────────────────────────────────────────

/// Extracts the MLS listing number from the Redfin page.
///
/// Redfin surfaces MLS in two places:
///   1. `<span class="ListingSource--mlsId">#R3090427</span>`
///   2. Page title: `"… MLS# R3090427 | Redfin"`
fn extract_mls_number(document: &Html) -> Option<String> {
    // 1. Try the dedicated CSS selector first.
    if let Ok(sel) = scraper::Selector::parse(".ListingSource--mlsId") {
        if let Some(el) = document.select(&sel).next() {
            let text: String = el.text().collect::<String>().trim().to_string();
            let cleaned = text.strip_prefix('#').unwrap_or(&text);
            if !cleaned.is_empty() {
                return Some(cleaned.to_string());
            }
        }
    }
    // 2. Fall back to the page title pattern: "MLS# R3090427"
    if let Ok(title_sel) = scraper::Selector::parse("title") {
        let title_text: String = document
            .select(&title_sel)
            .next()?
            .text()
            .collect::<String>();
        let re = Regex::new(r"MLS#?\s*([A-Z]\d+)").ok()?;
        return re
            .captures(&title_text)
            .and_then(|c| c.get(1))
            .map(|m| m.as_str().to_string());
    }
    None
}

// ── Entry point ───────────────────────────────────────────────────────────────

/// Parses a Redfin listing page into a `ParsedListing`.
/// Returns `None` if the page does not contain a `RealEstateListing` JSON-LD block.
pub fn parse(url: &str, html: &str) -> Option<ParsedListing> {
    let document = Html::parse_document(html);
    let json_ld = extract_json_ld(&document);
    let title = extract_title(&document);

    let mut property = extract_property(url, &title, &json_ld)?;
    property.mls_number = extract_mls_number(&document);

    property.land_sqft = extract_lot_size(html);
    property.property_tax = extract_property_tax(html);
    property.hoa_monthly = extract_hoa_monthly(html);
    property.source_status = extract_source_status(html);
    if let Some(carport_spaces) = extract_carport_spaces(html) {
        property.parking_carport = Some(carport_spaces);
        if property.parking_total.is_none() {
            property.parking_total = Some(carport_spaces);
        }
    }
    if let Some(schools) = extract_schools(html) {
        if let Some(e) = schools.elementary {
            property.school_elementary = Some(e.name);
            property.school_elementary_rating = e.rating;
        }
        if let Some(e) = schools.middle {
            property.school_middle = Some(e.name);
            property.school_middle_rating = e.rating;
        }
        if let Some(e) = schools.secondary {
            property.school_secondary = Some(e.name);
            property.school_secondary_rating = e.rating;
        }
    }

    let image_urls = extract_image_urls(&json_ld);
    if image_urls.is_empty() {
        tracing::info!(
            "redfin::parse: no images in JSON-LD for {} (sold/off-market listing?)",
            url
        );
    } else {
        tracing::debug!("redfin::parse: found {} image URL(s) for {}", image_urls.len(), url);
    }

    // Derive year from listed_date ("2026-02-24" → 2026) for date resolution.
    let year = property
        .listed_date
        .as_deref()
        .and_then(|d: &str| d.split('-').next())
        .and_then(|y: &str| y.parse::<i32>().ok())
        .unwrap_or(2026);
    let open_houses = extract_open_houses(&document, year);

    Some(ParsedListing {
        property,
        image_urls,
        open_houses,
    })
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsers::test_support::{fixture, listing_to_property, listing_to_snapshot};

    #[test]
    fn redfin_829_e14th() {
        let html =
            std::fs::read_to_string(fixture("redfin_829_e14th.html")).expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/829-E-14th-Ave-V5T-2N5/home/155809679",
            &html,
        )
        .expect("parse failed");
        insta::assert_json_snapshot!("redfin_829_e14th", listing_to_property(listing));
    }

    #[test]
    fn redfin_788_w8th() {
        let html =
            std::fs::read_to_string(fixture("redfin_788_w8th.html")).expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/788-W-8th-Ave-V5Z-1E1/home/",
            &html,
        )
        .expect("parse failed");
        let property = listing_to_property(listing);
        assert_eq!(property.hoa_monthly, Some(1137), "hoa_monthly");
        insta::assert_json_snapshot!("redfin_788_w8th", property);
    }

    #[test]
    fn redfin_3545_w_king_edward_carport() {
        let html = std::fs::read_to_string(fixture(
            "3545 W King Edward Ave, Vancouver, BC V6S 1M4 _ MLS# R3092688 _ Redfin.html",
        ))
        .expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/3545-W-King-Edward-Ave-V6S-1M4/home/155797202",
            &html,
        )
        .expect("parse failed");
        let property = listing_to_property(listing);
        assert_eq!(property.parking_carport, Some(1), "parking_carport");
        assert_eq!(property.parking_total, Some(1), "parking_total");
        assert_eq!(property.parking_garage, None, "parking_garage");
        insta::assert_json_snapshot!("redfin_3545_w_king_edward_carport", property);
    }

    #[test]
    fn redfin_2748_e23rd() {
        let html = std::fs::read_to_string(fixture(
            "2748 E 23rd Ave, Vancouver, BC V5R 1A7 _ MLS# R3088944 _ Redfin.html",
        ))
        .expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/2748-E-23rd-Ave-V5R-1A7/home/154849597",
            &html,
        )
        .expect("parse failed");
        insta::assert_json_snapshot!("redfin_2748_e23rd", listing_to_snapshot(listing));
    }

    #[test]
    fn redfin_3206_e25th() {
        let html = std::fs::read_to_string(fixture(
            "3206 E 25th Ave, Vancouver, BC V5R 1J6 _ MLS# R3093182 _ Redfin.html",
        ))
        .expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/3206-E-25th-Ave-V5R-1J6/home/154634866",
            &html,
        )
        .expect("parse failed");
        insta::assert_json_snapshot!("redfin_3206_e25th", listing_to_snapshot(listing));
    }

    #[test]
    fn redfin_2643_e8th_off_market() {
        let html = std::fs::read_to_string(fixture(
            "2643 E 8th Ave, Vancouver, BC V5M 1W4 _ Redfin.html",
        ))
        .expect("fixture not found");
        let listing = parse(
            "https://www.redfin.ca/bc/vancouver/2643-E-8th-Ave-V5M-1W4/home/155349348",
            &html,
        )
        .expect("parse failed");
        insta::assert_json_snapshot!("redfin_2643_e8th_off_market", listing_to_snapshot(listing));
    }
}
