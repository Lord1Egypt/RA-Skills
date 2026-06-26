//! Realtor.ca listing parser.
//!
//! Realtor.ca uses Imperva Incapsula bot protection that blocks plain HTTP
//! clients.  The backend falls back to Safari via AppleScript to obtain the
//! rendered DOM.
//!
//! Once we have the HTML, data is extracted from:
//!
//!   1. **JSON-LD `Product` block** — price, currency, description, SKU.
//!   2. **JSON-LD `Event` blocks** — address and coordinates (from open-house events).
//!   3. **CSS selectors** on `#propertyDetailsSectionContentSubCon_*` elements —
//!      sqft, year built, land size, parking, property tax.
//!   4. **Quick-stats icons** — bedrooms, bathrooms.
//!   5. **Page title** — MLS number.

use regex::Regex;
use scraper::{Html, Selector};
use serde_json::Value as JsonValue;

use super::{extract_json_ld, OpenHouseEvent, ParsedListing};
use crate::models::property::StoredProperty;

// ── Helpers ──────────────────────────────────────────────────────────────────

/// Strip currency symbols, commas, spaces and parse as i64.
fn parse_money(s: &str) -> Option<i64> {
    let clean: String = s.chars().filter(|c| c.is_ascii_digit() || *c == '.').collect();
    clean.parse::<f64>().ok().map(|v| v as i64)
}

/// Strip non-digit chars and parse as i64.
fn parse_int(s: &str) -> Option<i64> {
    let clean: String = s.chars().filter(|c| c.is_ascii_digit()).collect();
    clean.parse().ok()
}

/// Extract text from an element selected by `selector_str` within the document.
fn select_text(document: &Html, selector_str: &str) -> Option<String> {
    let sel = Selector::parse(selector_str).ok()?;
    document
        .select(&sel)
        .next()
        .map(|el| el.text().collect::<String>().trim().to_string())
        .filter(|s| !s.is_empty())
}

/// Extract the text of the value div inside a `#propertyDetailsSectionContentSubCon_<id>` block.
fn detail_value(document: &Html, field_id: &str) -> Option<String> {
    let sel_str = format!("#{field_id} .propertyDetailsSectionContentValue");
    select_text(document, &sel_str)
}

// ── Address from Event JSON-LD ───────────────────────────────────────────────

struct AddressInfo {
    street_address: Option<String>,
    city: Option<String>,
    region: Option<String>,
    postal_code: Option<String>,
    lat: Option<f64>,
    lon: Option<f64>,
}

fn extract_address(json_ld: &[JsonValue]) -> AddressInfo {
    // Event blocks contain the address/geo for the property.
    for block in json_ld {
        if block.get("@type").and_then(|t| t.as_str()) != Some("Event") {
            continue;
        }
        let location = match block.get("location") {
            Some(loc) => loc,
            None => continue,
        };
        let addr = location.get("address").unwrap_or(location);
        let geo = location.get("geo");

        return AddressInfo {
            street_address: addr
                .get("streetAddress")
                .and_then(|v| v.as_str())
                .map(titlecase),
            city: addr
                .get("addressLocality")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string()),
            region: addr
                .get("addressRegion")
                .and_then(|v| v.as_str())
                .map(region_abbrev),
            postal_code: addr
                .get("postalCode")
                .and_then(|v| v.as_str())
                .map(format_postal_code),
            lat: geo
                .and_then(|g| g.get("latitude"))
                .and_then(|v| v.as_str().and_then(|s| s.parse().ok()).or_else(|| v.as_f64())),
            lon: geo
                .and_then(|g| g.get("longitude"))
                .and_then(|v| v.as_str().and_then(|s| s.parse().ok()).or_else(|| v.as_f64())),
        };
    }

    AddressInfo {
        street_address: None,
        city: None,
        region: None,
        postal_code: None,
        lat: None,
        lon: None,
    }
}

/// Attempt to read a bare address string from the open‑graph description tag.
///
/// realtor.ca always includes a meta property "og:description" containing a
/// comma‑separated address (street, city, region [postal]).  This isn't as
/// reliable as the JSON‑LD blocks, but it serves as a useful fallback when the
/// page has no `Event` data (for example, no open houses).
fn extract_address_from_og(document: &Html) -> AddressInfo {
    if let Ok(sel) = Selector::parse("meta[property='og:description']") {
        for el in document.select(&sel) {
            if let Some(content) = el.value().attr("content") {
                let parts: Vec<&str> = content.split(',').map(|s| s.trim()).collect();
                if parts.len() >= 3 {
                    let street = Some(parts[0].to_string());
                    let city = Some(parts[1].to_string());
                    let last = parts[2];
                    // last part may contain region + postal, e.g. "British Columbia   V6S1M4"
                    let tokens: Vec<&str> = last.split_whitespace().collect();
                    let region = tokens.get(0).map(|s| region_abbrev(s));
                    let postal = tokens.last().map(|s| format_postal_code(s));
                    return AddressInfo {
                        street_address: street,
                        city,
                        region,
                        postal_code: postal,
                        lat: None,
                        lon: None,
                    };
                }
            }
        }
    }
    AddressInfo {
        street_address: None,
        city: None,
        region: None,
        postal_code: None,
        lat: None,
        lon: None,
    }
}

/// Naively scrape latitude/longitude numbers from the page's Javascript
/// dataLayer (or other inline JSON) when the normal JSON-LD events do not
/// provide coordinates. This is a best-effort fallback and expects the values
/// to appear as quoted strings.
fn extract_geo_from_html(html: &str) -> (Option<f64>, Option<f64>) {
    // 1. Search for explicit latitude/longitude strings in JS-like syntax.
    let lat_re = Regex::new(r#"latitude\s*[:=]\s*\\?\"?([-0-9\.]+)\\?\"?"#).unwrap();
    let lon_re = Regex::new(r#"longitude\s*[:=]\s*\\?\"?([-0-9\.]+)\\?\"?"#).unwrap();
    if let (Some(lat), Some(lon)) = (
        lat_re
            .captures(html)
            .and_then(|c| c.get(1))
            .and_then(|m| m.as_str().parse().ok()),
        lon_re
            .captures(html)
            .and_then(|c| c.get(1))
            .and_then(|m| m.as_str().parse().ok()),
    ) {
        return (Some(lat), Some(lon));
    }

    // 2. Look for a Google maps directions URL with destination=lat%2clon
    let map_re = Regex::new(r"destination=([0-9\.-]+)%2c([0-9\.-]+)").unwrap();
    if let Some(capt) = map_re.captures(html) {
        if let (Some(lat_s), Some(lon_s)) = (capt.get(1), capt.get(2)) {
            if let (Ok(lat), Ok(lon)) = (lat_s.as_str().parse(), lon_s.as_str().parse()) {
                return (Some(lat), Some(lon));
            }
        }
    }

    (None, None)
}

/// Extract open house events (startDate / endDate) from all Event JSON-LD blocks.
fn extract_open_houses(json_ld: &[JsonValue]) -> Vec<OpenHouseEvent> {
    let mut events = Vec::new();
    for block in json_ld {
        if block.get("@type").and_then(|t| t.as_str()) != Some("Event") {
            continue;
        }
        if let Some(start) = block.get("startDate").and_then(|v| v.as_str()) {
            events.push(OpenHouseEvent {
                start_time: start.to_string(),
                end_time: block
                    .get("endDate")
                    .and_then(|v| v.as_str())
                    .map(|s| s.to_string()),
            });
        }
    }
    events
}

/// Convert "BRITISH COLUMBIA" → "BC", etc.  Pass through short forms.
fn region_abbrev(s: &str) -> String {
    match s.trim().to_uppercase().as_str() {
        "BRITISH COLUMBIA" => "BC".to_string(),
        "ALBERTA" => "AB".to_string(),
        "ONTARIO" => "ON".to_string(),
        "QUEBEC" | "QUÉBEC" => "QC".to_string(),
        "MANITOBA" => "MB".to_string(),
        "SASKATCHEWAN" => "SK".to_string(),
        "NOVA SCOTIA" => "NS".to_string(),
        "NEW BRUNSWICK" => "NB".to_string(),
        other => other.to_string(),
    }
}

/// Convert "V6S1M4" → "V6S 1M4" (add space if missing in Canadian postal code).
fn format_postal_code(s: &str) -> String {
    let s = s.trim().to_uppercase();
    if s.len() == 6 && !s.contains(' ') {
        format!("{} {}", &s[..3], &s[3..])
    } else {
        s
    }
}

/// Convert "3545 W KING EDWARD AVENUE" → "3545 W King Edward Avenue".
fn titlecase(s: &str) -> String {
    s.split_whitespace()
        .map(|w| {
            let mut chars = w.chars();
            match chars.next() {
                None => String::new(),
                Some(c) => {
                    let upper: String = c.to_uppercase().collect();
                    upper + &chars.as_str().to_lowercase()
                }
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

// ── Product JSON-LD ──────────────────────────────────────────────────────────

struct ProductInfo {
    price: Option<i64>,
    currency: Option<String>,
    description: Option<String>,
    property_type: Option<String>,
}

fn extract_product(json_ld: &[JsonValue]) -> ProductInfo {
    for block in json_ld {
        if block.get("@type").and_then(|t| t.as_str()) != Some("Product") {
            continue;
        }

        let offer = block
            .get("offers")
            .and_then(|o| if o.is_array() { o.get(0) } else { Some(o) });

        let price = offer
            .and_then(|o| o.get("price"))
            .and_then(|v| {
                v.as_f64()
                    .or_else(|| v.as_str().and_then(|s| s.parse::<f64>().ok()))
            })
            .map(|p| p as i64);

        let currency = offer
            .and_then(|o| o.get("priceCurrency"))
            .and_then(|v| v.as_str())
            .map(|s| s.to_string());

        let description = block
            .get("description")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string());

        let category = block
            .get("category")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string());

        return ProductInfo {
            price,
            currency,
            description,
            property_type: category,
        };
    }

    ProductInfo {
        price: None,
        currency: None,
        description: None,
        property_type: None,
    }
}

// ── HTML detail extraction ───────────────────────────────────────────────────

/// Extract MLS number from the page title: "... - R3092688 | REALTOR.ca"
fn extract_mls(document: &Html) -> Option<String> {
    // Try the dedicated element first.
    if let Some(mls) = select_text(document, "#MLNumberVal") {
        return Some(mls);
    }
    // Fall back to page title.
    let title = select_text(document, "title")?;
    let re = Regex::new(r"[- ](R\d{5,})").ok()?;
    re.captures(&title)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

/// Extract bedroom/bathroom counts from the quick-reference icons.
fn extract_quick_stats(document: &Html) -> (Option<i64>, Option<i64>) {
    let sel = Selector::parse(".listingIconNum").unwrap();
    let nums: Vec<String> = document
        .select(&sel)
        .map(|el| el.text().collect::<String>().trim().to_string())
        .collect();

    let beds = nums.first().and_then(|s| s.parse().ok());
    let baths = nums.get(1).and_then(|s| s.parse().ok());
    (beds, baths)
}

/// Extract all highres image URLs from the page.
fn extract_image_urls(document: &Html, html: &str) -> Vec<String> {
    // Strategy 1: regex for highres CDN URLs in full HTML.
    let re =
        Regex::new(r#"https://cdn\.realtor\.ca/listing/[^"'\s]*?/highres/[^"'\s]+"#).unwrap();
    let mut seen = std::collections::HashSet::new();
    let mut urls = Vec::new();
    for m in re.find_iter(html) {
        let url = m.as_str().to_string();
        if seen.insert(url.clone()) {
            urls.push(url);
        }
    }
    if !urls.is_empty() {
        return urls;
    }

    // Strategy 2: og:image meta tag.
    if let Ok(sel) = Selector::parse("meta[property='og:image']") {
        for el in document.select(&sel) {
            if let Some(url) = el.value().attr("content") {
                urls.push(url.to_string());
            }
        }
    }
    urls
}

// ── Main parse function ──────────────────────────────────────────────────────

pub fn parse(url: &str, html: &str) -> Option<ParsedListing> {
    if html.len() < 5000 {
        return None; // Too small to be a real listing page.
    }

    let document = Html::parse_document(html);
    let json_ld = extract_json_ld(&document);

    let mut addr = extract_address(&json_ld);
    let open_houses = extract_open_houses(&json_ld);
    // If JSON-LD events failed to provide an address, fall back to parsing the
    // og:description meta tag which contains a comma‑separated address string.
    if addr.street_address.is_none() && addr.city.is_none() {
        let og_addr = extract_address_from_og(&document);
        if og_addr.street_address.is_some() || og_addr.city.is_some() {
            addr = og_addr;
        }
    }
    // coordinates may also be missing; try a loose regex over the raw HTML.
    if addr.lat.is_none() || addr.lon.is_none() {
        let (lat, lon) = extract_geo_from_html(html);
        if addr.lat.is_none() {
            addr.lat = lat;
        }
        if addr.lon.is_none() {
            addr.lon = lon;
        }
    }
    let product = extract_product(&json_ld);
    let (beds, baths) = extract_quick_stats(&document);
    let mls = extract_mls(&document);

    // Detail fields from CSS selectors.
    let sqft = detail_value(&document, "propertyDetailsSectionContentSubCon_SquareFootage")
        .and_then(|s| parse_int(&s));
    let year_built = detail_value(&document, "propertyDetailsSectionContentSubCon_BuiltIn")
        .and_then(|s| parse_int(&s));
    let land_sqft = detail_value(&document, "propertyDetailsSectionContentSubCon_LandSize")
        .and_then(|s| parse_int(&s));
    let property_tax =
        detail_value(&document, "propertyDetailsSectionContentSubCon_AnnualPropertyTaxes")
            .and_then(|s| parse_money(&s));

    // Title: "Street, City — Beds bd / Baths ba"
    let title = match (&addr.street_address, &addr.city, beds, baths) {
        (Some(street), Some(city), Some(b), Some(ba)) => {
            format!("{street}, {city} - {b} beds/{ba} baths")
        }
        (Some(street), Some(city), _, _) => format!("{street}, {city}"),
        _ => product
            .description
            .as_deref()
            .unwrap_or("")
            .chars()
            .take(80)
            .collect(),
    };

    let image_urls = extract_image_urls(&document, html);

    // If we got nothing useful, bail out.
    if product.price.is_none() && beds.is_none() && addr.street_address.is_none() {
        return None;
    }

    Some(ParsedListing {
        open_houses,
        property: StoredProperty {
            id: 0,
            search_profile_id: None, // overwritten by caller
            title,
            description: product.description.unwrap_or_default(),
            price: product.price,
            price_currency: product.currency,
            offer_price: None,
            street_address: addr.street_address,
            city: addr.city,
            region: addr.region,
            postal_code: addr.postal_code,
            country: Some("CA".to_string()),
            lat: addr.lat,
            lon: addr.lon,
            bedrooms: beds,
            bathrooms: baths,
            sqft,
            year_built,
            land_sqft,
            property_type: product.property_type,
            parking_total: None,
            parking_garage: None,
            parking_carport: None,
            parking_pad: None,
            property_tax,
            hoa_monthly: None,
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
            monthly_total: None,
            monthly_cost: None,
            has_rental_suite: None,
            rental_income: None,
            school_elementary: None,
            school_elementary_rating: None,
            school_middle: None,
            school_middle_rating: None,
            school_secondary: None,
            school_secondary_rating: None,
            mls_number: mls,
            listed_date: None,
            status: crate::models::property::ListingStatus::Interested,
            redfin_url: None,
            realtor_url: Some(url.to_string()),
            rew_url: None,
            zillow_url: None,
            notes: None,
            created_at: String::new(),
            updated_at: None,
        },
        image_urls,
    })
}

// ── Tests ────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsers::test_support::{fixture, listing_to_snapshot};

    #[test]
    fn realtor_3545_w_king_edward() {
        let html =
            std::fs::read_to_string(fixture("realtor_3545_w_king_edward.html")).unwrap();
        let listing = parse(
            "https://www.realtor.ca/real-estate/29391064/3545-w-king-edward-avenue-vancouver",
            &html,
        )
        .expect("should parse realtor.ca listing");
        insta::assert_json_snapshot!(listing_to_snapshot(listing));
    }

    /// If the page has no JSON-LD `Event` blocks (e.g. no open houses), we still
    /// want to recover the street/city/region using the OG description meta tag.
    #[test]
    fn test_address_fallback_from_og() {
        // The parser bails early if the HTML string is very short, so ensure we
        // create a long document by padding with dummy content.
        let mut html = r#"<html><head>
            <meta property='og:description' content='123 Main St, Smalltown, Ontario V1A2B3'>
        </head><body>"#.to_string();
        html.push_str(&"x".repeat(6000));
        html.push_str("</body></html>");
        let listing = parse("https://www.realtor.ca/real-estate/foo", &html)
            .expect("parse should succeed even with minimal html");
        assert_eq!(listing.property.street_address.as_deref(), Some("123 Main St"));
        assert_eq!(listing.property.city.as_deref(), Some("Smalltown"));
        assert_eq!(listing.property.region.as_deref(), Some("ON"));
        assert_eq!(listing.property.postal_code.as_deref(), Some("V1A 2B3"));
    }

    #[test]
    fn test_geo_extraction_fallback() {
        // case A: coordinates buried in a JS object
        let mut html = r#"<html><head></head><body>"#.to_string();
        html.push_str(r#"<script>var foo={latitude:"49.1",longitude:"-123.2"};</script>"#);
        html.push_str(r#"<meta property='og:description' content='123 Main St, Nowhere, BC V0X0X0'>"#);
        html.push_str(&"x".repeat(6000));
        html.push_str("</body></html>");
        let listing = parse("https://www.realtor.ca/real-estate/foo", &html).unwrap();
        assert_eq!(listing.property.lat, Some(49.1));
        assert_eq!(listing.property.lon, Some(-123.2));

        // case B: use a google maps directions link
        let mut html2 = r#"<html><head></head><body>"#.to_string();
        html2.push_str(
            r#"<a id='listingDirectionsBtn' href='https://www.google.com/maps/dir/?api=1&destination=51.2%2c-122.3'>"#,
        );
        html2.push_str(r#"<meta property='og:description' content='A,B,C'>"#);
        html2.push_str(&"x".repeat(6000));
        html2.push_str("</body></html>");
        let listing2 = parse("https://www.realtor.ca/real-estate/bar", &html2).unwrap();
        assert_eq!(listing2.property.lat, Some(51.2));
        assert_eq!(listing2.property.lon, Some(-122.3));
    }


}
