//! rew.ca listing parser.
//!
//! rew.ca renders a standard server-side HTML page (no bot protection like realtor.ca).
//! Structured data comes from two places:
//!   1. A `SingleFamilyResidence` JSON-LD block — address, coordinates, URL.
//!   2. Inline HTML sections — price, tax, bedrooms, bathrooms, year built, lot size,
//!      parking, strata fee, and images.
//!
//! The JSON-LD does NOT include price, tax, or most property facts, so we
//! parse the HTML directly for those using CSS selectors.

use scraper::{Html, Selector};
use serde_json::Value as JsonValue;

use super::{extract_description, extract_json_ld, extract_title, ParsedListing};
use crate::models::property::StoredProperty;

// ── Field helpers ─────────────────────────────────────────────────────────────

/// Strip currency symbols and commas, parse as i64.
pub fn parse_money_i64(s: &str) -> Option<i64> {
    let clean: String = s
        .chars()
        .filter(|c| c.is_ascii_digit() || *c == '.')
        .collect();
    clean.parse::<f64>().ok().map(|v| v as i64)
}

/// Strip non-numeric chars, parse as i64.
fn parse_int(s: &str) -> Option<i64> {
    let clean: String = s.chars().filter(|c| c.is_ascii_digit()).collect();
    clean.parse().ok()
}

// ── Section parser ────────────────────────────────────────────────────────────

/// Find a labelled value in `<section><div>LABEL</div><div>VALUE</div></section>` blocks.
/// Walks each `<section>` element: if its first child div's text matches, return the
/// text of the second child div.
fn find_section_value(document: &Html, label: &str) -> Option<String> {
    find_section_value_pred(document, |t| t == label)
}

/// Like `find_section_value` but matches if the label contains `label_substr`.
pub fn find_section_value_contains(document: &Html, label_substr: &str) -> Option<String> {
    find_section_value_pred(document, |t| t.contains(label_substr))
}

fn find_section_value_pred<F: Fn(&str) -> bool>(document: &Html, pred: F) -> Option<String> {
    let section_sel = Selector::parse("section").unwrap();
    let div_sel = Selector::parse("div").unwrap();

    for section in document.select(&section_sel) {
        let divs: Vec<_> = section.select(&div_sel).collect();
        if divs.len() < 2 {
            continue;
        }
        // Only look at top-level child divs (depth 1 inside section)
        let label_text = divs[0].text().collect::<String>();
        if pred(label_text.trim()) {
            // Value is in the second top-level div
            let val = divs[1].text().collect::<String>();
            let val = val.trim().to_string();
            if !val.is_empty() {
                return Some(val);
            }
        }
    }
    None
}

// ── JSON-LD helpers ───────────────────────────────────────────────────────────

fn find_residence(json_ld: &[JsonValue]) -> Option<&JsonValue> {
    json_ld.iter().find(|v| {
        let t = v["@type"].as_str().unwrap_or("");
        t.contains("Residence") || t.contains("House") || t.contains("Apartment")
    })
}

// ── Image extraction ──────────────────────────────────────────────────────────

fn extract_image_urls(document: &Html) -> Vec<String> {
    // Primary: parse the `data-photos` JSON attribute on the gallery container.
    // REW embeds the canonical listing photo list as:
    //   data-photos='[{"url":"https://assets-listings.rew.ca/…"},…]'
    // This is authoritative and excludes ads / similar-listing carousels that
    // also use the assets-listings.rew.ca domain.
    let photos_sel = Selector::parse("[data-photos]").unwrap();
    if let Some(el) = document.select(&photos_sel).next() {
        if let Some(raw_json) = el.value().attr("data-photos") {
            if let Ok(serde_json::Value::Array(arr)) =
                serde_json::from_str::<serde_json::Value>(raw_json)
            {
                let mut seen = std::collections::HashSet::new();
                let mut out = Vec::new();
                for entry in &arr {
                    if let Some(url) = entry["url"].as_str() {
                        // Strip Imgix query params to get the full-resolution original.
                        let clean = url.split('?').next().unwrap_or(url);
                        if !clean.is_empty() && seen.insert(clean.to_string()) {
                            out.push(clean.to_string());
                        }
                    }
                }
                if !out.is_empty() {
                    return out;
                }
            }
        }
    }

    // Fallback: scan img tags (used when data-photos is absent).
    // rew.ca images appear in two forms depending on how the page was captured:
    //   - Lazy-loaded (browser save): `data-src="https://assets-listings.rew.ca/…?fill=blur&w=753…"`
    //   - Directly served (curl): `src="https://assets-listings.rew.ca/…?w=750…"`
    // In both cases the URL has Imgix sizing/quality params that limit resolution.
    // Stripping the query string yields the full-resolution original.
    let sel = Selector::parse(
        "img[data-src*='assets-listings.rew.ca'], img[src*='assets-listings.rew.ca']",
    )
    .unwrap();
    let mut seen = std::collections::HashSet::new();
    let mut out = Vec::new();
    for el in document.select(&sel) {
        let raw = el
            .value()
            .attr("data-src")
            .or_else(|| el.value().attr("src"))
            .unwrap_or("");
        // Strip Imgix query params to get the full-resolution original.
        let clean = raw.split('?').next().unwrap_or(raw);
        if !clean.is_empty() && seen.insert(clean.to_string()) {
            out.push(clean.to_string());
        }
    }
    out
}

// ── MLS number extraction ────────────────────────────────────────────────────

/// Extracts the MLS® listing number from the page's description meta tag.
/// REW includes it as "MLS® # RXXXXXXX" at the end of the description.
fn extract_mls_number(document: &Html) -> Option<String> {
    let sel = Selector::parse("meta[name='description']").unwrap();
    let content = document
        .select(&sel)
        .next()
        .and_then(|el| el.value().attr("content"))?;
    let re = regex::Regex::new(r"MLS[^\s]*\s*#?\s*([A-Z]\d+)").ok()?;
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

// ── Property type extraction ──────────────────────────────────────────────────

/// Extracts the property type from the page's description meta tag.
/// REW formats it as "Browse N photos of this TYPE in NEIGHBOURHOOD…".
fn extract_property_type(document: &Html) -> Option<String> {
    let sel = Selector::parse("meta[name='description']").unwrap();
    let content = document
        .select(&sel)
        .next()
        .and_then(|el| el.value().attr("content"))?;
    let re = regex::Regex::new(r"(?i)Browse \d+ photos of this ([\w ]+?) in ").ok()?;
    re.captures(content)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().trim().to_string())
}

// ── Floor area (sqft) extraction ─────────────────────────────────────────────

/// Extracts interior floor area from the `data-listing-sqft` attribute on the
/// summary list item, falling back to the meta description "is N Sqft" pattern.
fn extract_sqft(document: &Html) -> Option<i64> {
    // Primary: <li data-listing-sqft="1560">…</li>
    let sel = Selector::parse("li[data-listing-sqft]").unwrap();
    if let Some(el) = document.select(&sel).next() {
        if let Some(v) = el.value().attr("data-listing-sqft") {
            if let Ok(n) = v.trim().parse::<i64>() {
                if n > 0 {
                    return Some(n);
                }
            }
        }
    }
    // Fallback: "This property features N beds, M baths and is N Sqft."
    let desc_sel = Selector::parse("meta[name='description']").unwrap();
    let content = document
        .select(&desc_sel)
        .next()
        .and_then(|el| el.value().attr("content"))?;
    let re = regex::Regex::new(r"(?i)is ([\d,]+)\s*sqft").ok()?;
    re.captures(content)
        .and_then(|c| c.get(1))
        .and_then(|m| parse_int(m.as_str()))
}

// ── Price extraction ──────────────────────────────────────────────────────────

/// rew.ca renders price as: <div class='mr-3 5'>$2,488,800</div>
fn extract_price(document: &Html) -> Option<i64> {
    // Try the "List Price" section first
    if let Some(raw) = find_section_value(document, "List Price") {
        // The value div may contain nested elements; grab text starting with $
        let price_str: String = raw
            .chars()
            .take_while(|c| c.is_ascii_digit() || *c == '$' || *c == ',')
            .collect();
        if let Some(v) = parse_money_i64(&price_str) {
            return Some(v);
        }
    }

    // Fallback: look for the styled price div
    let sel = Selector::parse("div.mr-3").unwrap();
    for el in document.select(&sel) {
        let text = el.text().collect::<String>();
        let text = text.trim();
        if text.starts_with('$') {
            if let Some(v) = parse_money_i64(text) {
                return Some(v);
            }
        }
    }
    None
}
// ── Address extraction ────────────────────────────────────────────────────────

/// Parsed address and geo fields from a JSON-LD Residence node.
#[derive(Default)]
struct AddressInfo {
    street_address: Option<String>,
    city: Option<String>,
    region: Option<String>,
    postal_code: Option<String>,
    lat: Option<f64>,
    lon: Option<f64>,
}

fn extract_address(residence: Option<&JsonValue>) -> AddressInfo {
    let Some(r) = residence else {
        return AddressInfo::default();
    };
    let addr = &r["address"];
    AddressInfo {
        street_address: addr["streetAddress"].as_str().map(str::to_string),
        city: addr["addressLocality"].as_str().map(str::to_string),
        region: addr["addressRegion"].as_str().map(str::to_string),
        postal_code: addr["postalCode"].as_str().map(str::to_string),
        lat: r["geo"]["latitude"].as_f64(),
        lon: r["geo"]["longitude"].as_f64(),
    }
}

struct ParkingInfo {
    parking_total: Option<i64>,
    parking_garage: Option<i64>,
    parking_carport: Option<i64>,
    parking_pad: Option<i64>,
}

fn parse_parking_info(document: &Html) -> ParkingInfo {
    let total = find_section_value(document, "Parking Spaces").and_then(|s| parse_int(&s));

    let details = find_section_value(document, "Parking Details")
        .unwrap_or_default()
        .to_lowercase();

    let has_garage = details.contains("garage");
    let has_carport = details.contains("carport") || details.contains("covered");
    let has_open =
        details.contains("open") || details.contains("pad") || details.contains("driveway");
    let category_count = (has_garage as u8) + (has_carport as u8) + (has_open as u8);

    if let Some(total_spaces) = total {
        if category_count == 1 {
            return ParkingInfo {
                parking_total: Some(total_spaces),
                parking_garage: if has_garage { Some(total_spaces) } else { None },
                parking_carport: if has_carport {
                    Some(total_spaces)
                } else {
                    None
                },
                parking_pad: if has_open { Some(total_spaces) } else { None },
            };
        }
        return ParkingInfo {
            parking_total: Some(total_spaces),
            parking_garage: None,
            parking_carport: None,
            parking_pad: None,
        };
    }

    ParkingInfo {
        parking_total: None,
        parking_garage: None,
        parking_carport: None,
        parking_pad: None,
    }
}
// ── Entry point ───────────────────────────────────────────────────────────────

/// Parses a rew.ca listing page into a full `ParsedListing`.
/// Returns `None` if the URL is not rew.ca or no recognisable data is found.
pub fn parse(url: &str, html: &str) -> Option<ParsedListing> {
    if !url.contains("rew.ca") {
        return None;
    }

    let document = Html::parse_document(html);
    let json_ld = extract_json_ld(&document);
    let title = extract_title(&document);
    let description = extract_description(&document);

    let residence = find_residence(&json_ld);

    // ── Address (from JSON-LD SingleFamilyResidence) ──────────────────────────
    let addr = extract_address(residence);

    // ── Price ─────────────────────────────────────────────────────────────────
    let price = extract_price(&document);

    // ── Property tax — "Gross Taxes for YYYY" ─────────────────────────────────
    let property_tax =
        find_section_value_contains(&document, "Gross Taxes").and_then(|s| parse_money_i64(&s));

    // ── Home facts ────────────────────────────────────────────────────────────
    let bedrooms = find_section_value(&document, "Bedrooms").and_then(|s| parse_int(&s));

    let bathrooms = find_section_value(&document, "Full Bathrooms").and_then(|s| parse_int(&s));

    // Year built: "Built in 1927 (99 yrs old)"
    let year_built = find_section_value(&document, "Year Built").and_then(|s| {
        s.split_whitespace()
            .find_map(|tok| tok.parse::<i64>().ok().filter(|&y| y > 1800 && y < 2100))
    });

    // Lot size: "33 ft x 122 ft (4026 ft²)" — extract the sqft number in parens
    let land_sqft = find_section_value(&document, "Lot Size").and_then(|s| {
        // Look for number before "ft²" or "ft&sup2;"
        let re_pat = regex::Regex::new(r"\(([0-9,]+)\s*ft").ok()?;
        re_pat.captures(&s).and_then(|c| parse_int(&c[1]))
    });

    let parking = parse_parking_info(&document);

    // Strata / HOA fee.
    // Label variants seen in the wild:
    //   "Strata Fee"              — standard condo
    //   "Strata Maintenance Fees" — some rew.ca listings
    //   "Maintenance Fee"         — non-strata properties
    let hoa_monthly = find_section_value(&document, "Strata Fee")
        .or_else(|| find_section_value_contains(&document, "Strata Maintenance"))
        .or_else(|| find_section_value(&document, "Maintenance Fee"))
        .and_then(|s| parse_money_i64(&s));

    // ── Images ────────────────────────────────────────────────────────────────
    let image_urls = extract_image_urls(&document);

    let mls_number = extract_mls_number(&document);
    let property_type = extract_property_type(&document);
    let sqft = extract_sqft(&document);

    let property = StoredProperty {
        id: 0,
        search_profile_id: None, // overwritten by caller
        redfin_url: None,
        realtor_url: None,
        rew_url: Some(url.to_string()),
        zillow_url: None,
        title,
        description,
        price,
        price_currency: Some("CAD".to_string()),
        offer_price: None,
        street_address: addr.street_address,
        city: addr.city,
        region: addr.region,
        postal_code: addr.postal_code,
        country: Some("Canada".to_string()),
        property_type,
        bedrooms,
        bathrooms,
        sqft, // from data-listing-sqft attribute
        year_built,
        lat: addr.lat,
        lon: addr.lon,
        created_at: String::new(),
        updated_at: None,
        notes: None,
        parking_total: parking.parking_total,
        parking_garage: parking.parking_garage,
        parking_carport: parking.parking_carport,
        parking_pad: parking.parking_pad,
        land_sqft,
        property_tax,
        skytrain_station: None,
        skytrain_walk_min: None,
        radiant_floor_heating: None,
        ac: None,
        laundry_in_unit: None,
        source_status: None,
        agent_comment: None,
        down_payment_pct: None,
        mortgage_interest_rate: None,
        amortization_years: None,
        mortgage_monthly: None,
        hoa_monthly,
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
        listed_date: None,
        mls_number,
    };

    Some(ParsedListing {
        property,
        image_urls,
        open_houses: vec![],
    })
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsers::test_support::{fixture, listing_to_property};

    #[test]
    fn rew_788_w8th() {
        let html =
            std::fs::read_to_string(fixture("rew_788_w8th.html")).expect("fixture not found");
        let listing = parse(
            "https://www.rew.ca/properties/l01-788-w-8th-avenue-vancouver-bc",
            &html,
        )
        .expect("parse failed");
        let property = listing_to_property(listing);
        assert_eq!(property.hoa_monthly, Some(1137), "hoa_monthly");
        insta::assert_json_snapshot!("rew_788_w8th", property);
    }

    #[test]
    fn rew_3545_w_king_edward_carport() {
        let html = std::fs::read_to_string(fixture(
            "For Sale_ 3545 W King Edward Avenue, Vancouver, BC - REW.html",
        ))
        .expect("fixture not found");
        let listing = parse(
            "https://www.rew.ca/properties/3545-w-king-edward-avenue-vancouver-bc",
            &html,
        )
        .expect("parse failed");
        let property = listing_to_property(listing);
        assert_eq!(property.parking_carport, Some(1), "parking_carport");
        assert_eq!(property.parking_total, Some(1), "parking_total");
        assert_eq!(property.parking_garage, None, "parking_garage");
        insta::assert_json_snapshot!("rew_3545_w_king_edward_carport", property);
    }
}
