//! Zillow listing parser.
//!
//! Zillow uses PerimeterX bot protection (served via CloudFront).  The backend
//! falls back to Safari via AppleScript to obtain the rendered DOM.
//!
//! Once we have the HTML, data is extracted from:
//!
//!   1. **JSON-LD `RealEstateListing`** — price, currency, beds, sqft, address, geo.
//!   2. **`__NEXT_DATA__` script** — comprehensive property data including lot size,
//!      year built, parking, HOA, MLS number, images, and more.
//!   3. **Meta tags** — title (contains MLS#), description, og:image.

use regex::Regex;
use scraper::{Html, Selector};
use serde_json::Value as JsonValue;

use super::{extract_json_ld, ParsedListing};
use crate::models::property::StoredProperty;

// ── Helpers ──────────────────────────────────────────────────────────────────

fn json_str(v: &JsonValue, key: &str) -> Option<String> {
    v.get(key)
        .and_then(|v| v.as_str())
        .filter(|s| !s.is_empty())
        .map(|s| s.to_string())
}

fn json_i64(v: &JsonValue, key: &str) -> Option<i64> {
    v.get(key).and_then(|v| v.as_i64().or_else(|| v.as_f64().map(|f| f as i64)))
}

fn json_f64(v: &JsonValue, key: &str) -> Option<f64> {
    v.get(key).and_then(|v| v.as_f64().or_else(|| v.as_str().and_then(|s| s.parse().ok())))
}

fn parse_money(s: &str) -> Option<i64> {
    let clean: String = s.chars().filter(|c| c.is_ascii_digit() || *c == '.').collect();
    clean.parse::<f64>().ok().map(|v| v as i64)
}

// ── JSON-LD extraction ───────────────────────────────────────────────────────

struct JsonLdData {
    price: Option<i64>,
    currency: Option<String>,
    beds: Option<i64>,
    sqft: Option<i64>,
    street_address: Option<String>,
    city: Option<String>,
    region: Option<String>,
    postal_code: Option<String>,
    lat: Option<f64>,
    lon: Option<f64>,
}

fn extract_from_json_ld(json_ld: &[JsonValue]) -> JsonLdData {
    for block in json_ld {
        let typ = block.get("@type").and_then(|t| t.as_str()).unwrap_or("");
        if typ != "RealEstateListing" {
            continue;
        }

        let offer = block.get("offers");
        let item = offer.and_then(|o| o.get("itemOffered")).unwrap_or(block);
        let addr = item.get("address");
        let geo = item.get("geo");

        let price = offer
            .and_then(|o| o.get("price"))
            .and_then(|v| v.as_f64().or_else(|| v.as_str().and_then(|s| s.parse().ok())))
            .map(|p| p as i64);
        let currency = offer.and_then(|o| json_str(o, "priceCurrency"));

        let sqft = item
            .get("floorSize")
            .and_then(|fs| fs.get("value"))
            .and_then(|v| v.as_f64())
            .map(|v| v as i64);

        return JsonLdData {
            price,
            currency,
            beds: json_i64(item, "numberOfBedrooms"),
            sqft,
            street_address: addr.and_then(|a| json_str(a, "streetAddress")),
            city: addr.and_then(|a| json_str(a, "addressLocality")),
            region: addr.and_then(|a| json_str(a, "addressRegion")),
            postal_code: addr
                .and_then(|a| json_str(a, "postalCode"))
                .map(|s| format_postal_code(&s)),
            lat: geo.and_then(|g| json_f64(g, "latitude")),
            lon: geo.and_then(|g| json_f64(g, "longitude")),
        };
    }

    JsonLdData {
        price: None,
        currency: None,
        beds: None,
        sqft: None,
        street_address: None,
        city: None,
        region: None,
        postal_code: None,
        lat: None,
        lon: None,
    }
}

/// Convert "V6S1M4" → "V6S 1M4".
fn format_postal_code(s: &str) -> String {
    let s = s.trim().to_uppercase();
    if s.len() == 6 && !s.contains(' ') {
        format!("{} {}", &s[..3], &s[3..])
    } else {
        s
    }
}

// ── __NEXT_DATA__ extraction ─────────────────────────────────────────────────

struct NextData {
    year_built: Option<i64>,
    baths: Option<i64>,
    lot_sqft: Option<i64>,
    description: Option<String>,
    property_type: Option<String>,
    parking_total: Option<i64>,
    hoa_monthly: Option<i64>,
    property_tax: Option<i64>,
    mls_number: Option<String>,
    listed_date: Option<String>,
    images: Vec<String>,
}

fn extract_next_data(html: &str) -> NextData {
    let empty = NextData {
        year_built: None,
        baths: None,
        lot_sqft: None,
        description: None,
        property_type: None,
        parking_total: None,
        hoa_monthly: None,
        property_tax: None,
        mls_number: None,
        listed_date: None,
        images: vec![],
    };

    // Find the __NEXT_DATA__ JSON blob.
    let re = match Regex::new(r#"<script\s+id="__NEXT_DATA__"\s+type="application/json">(.*?)</script>"#) {
        Ok(re) => re,
        Err(_) => return empty,
    };
    let next_json = match re.captures(html).and_then(|c| c.get(1)) {
        Some(m) => m.as_str(),
        None => return empty,
    };
    let root: JsonValue = match serde_json::from_str(next_json) {
        Ok(v) => v,
        Err(_) => return empty,
    };

    // Navigate to the property object inside gdpClientCache.
    // Path: props.pageProps.componentProps.gdpClientCache.<first key>.property
    let gdp = root
        .pointer("/props/pageProps/componentProps/gdpClientCache")
        .or_else(|| root.pointer("/props/pageProps/gdpClientCache"));

    let property = gdp
        .and_then(|cache| {
            // gdpClientCache is an object with query-hash keys; grab the first one.
            if let Some(obj) = cache.as_object() {
                for (_key, val) in obj {
                    // Try parsing the value as JSON string (it's often double-encoded).
                    if let Some(s) = val.as_str() {
                        if let Ok(parsed) = serde_json::from_str::<JsonValue>(s) {
                            if parsed.get("property").is_some() {
                                return parsed.get("property").cloned();
                            }
                        }
                    }
                    // Or it might already be a direct object.
                    if val.get("property").is_some() {
                        return val.get("property").cloned();
                    }
                }
            }
            None
        });

    let prop = match property {
        Some(p) => p,
        None => return empty,
    };

    // Year built.
    let year_built = json_i64(&prop, "yearBuilt")
        .or_else(|| prop.get("resoFacts").and_then(|rf| json_i64(rf, "yearBuilt")));

    // Bathrooms — Zillow uses bathrooms (full) + bathroomsFull, bathroomsHalf.
    let baths = json_i64(&prop, "bathrooms")
        .or_else(|| prop.get("resoFacts").and_then(|rf| json_i64(rf, "bathroomsTotalInteger")));

    // Lot size in sqft.
    let lot_sqft = json_i64(&prop, "lotSize")
        .or_else(|| json_f64(&prop, "lotAreaValue").map(|v| v as i64))
        .or_else(|| {
            prop.get("resoFacts")
                .and_then(|rf| json_str(rf, "lotSize"))
                .and_then(|s| {
                    // "3,920 sqft" or "3920.4 Square Feet"
                    let clean: String = s.chars().filter(|c| c.is_ascii_digit() || *c == '.').collect();
                    clean.parse::<f64>().ok().map(|v| v as i64)
                })
        });

    // Description.
    let description = json_str(&prop, "description")
        .or_else(|| prop.get("homeDescription").and_then(|v| v.as_str()).map(|s| s.to_string()));

    // Property type.
    let property_type = json_str(&prop, "homeType")
        .or_else(|| prop.get("resoFacts").and_then(|rf| json_str(rf, "homeType")));

    // Parking.
    let parking_total = prop
        .get("resoFacts")
        .and_then(|rf| json_i64(rf, "parkingCapacity"));

    // HOA.
    let hoa_monthly = json_i64(&prop, "monthlyHoaFee")
        .or_else(|| {
            prop.get("resoFacts")
                .and_then(|rf| json_str(rf, "hoaFee"))
                .and_then(|s| parse_money(&s))
        });

    // Annual property tax.
    let property_tax = json_i64(&prop, "taxAnnualAmount")
        .or_else(|| {
            prop.get("propertyTaxRate")
                .and(None::<i64>) // rate alone isn't useful
        });

    // MLS number — from attributionInfo or palsId.
    let mls_number = prop
        .get("attributionInfo")
        .and_then(|ai| json_str(ai, "mlsId"))
        .or_else(|| {
            json_str(&prop, "palsId").and_then(|pals| {
                // palsId format: "13596001_R3092688" — MLS is after underscore.
                pals.split('_').nth(1).map(|s| s.to_string())
            })
        });

    // Listed date.
    let listed_date = prop
        .get("datePosted")
        .and_then(|v| v.as_str())
        .map(|s| s.chars().take(10).collect()); // "2026-02-23"

    // Images — from responsivePhotos or similar arrays.
    let mut images = Vec::new();
    if let Some(photos) = prop.get("responsivePhotos").and_then(|v| v.as_array()) {
        for photo in photos {
            // Each photo has mixedSources.jpeg[].url at various widths.
            if let Some(jpegs) = photo
                .pointer("/mixedSources/jpeg")
                .and_then(|v| v.as_array())
            {
                // Pick the largest JPEG.
                if let Some(best) = jpegs.last() {
                    if let Some(url) = best.get("url").and_then(|v| v.as_str()) {
                        images.push(url.to_string());
                    }
                }
            }
        }
    }

    // Fallback: originalPhotos.
    if images.is_empty() {
        if let Some(photos) = prop.get("originalPhotos").and_then(|v| v.as_array()) {
            for photo in photos {
                if let Some(url) = photo
                    .pointer("/mixedSources/jpeg")
                    .and_then(|v| v.as_array())
                    .and_then(|arr| arr.last())
                    .and_then(|v| v.get("url"))
                    .and_then(|v| v.as_str())
                {
                    images.push(url.to_string());
                }
            }
        }
    }

    NextData {
        year_built,
        baths,
        lot_sqft,
        description,
        property_type,
        parking_total,
        hoa_monthly,
        property_tax,
        mls_number,
        listed_date,
        images,
    }
}

// ── Meta-tag MLS extraction ──────────────────────────────────────────────────

/// Extract MLS# from title like "3545 King Edward ... | MLS #R3092688 | Zillow"
fn extract_mls_from_title(document: &Html) -> Option<String> {
    let sel = Selector::parse("title").ok()?;
    let title = document.select(&sel).next()?.text().collect::<String>();
    let re = Regex::new(r"MLS\s*#?\s*([A-Z0-9]+)").ok()?;
    re.captures(&title)
        .and_then(|c| c.get(1))
        .map(|m| m.as_str().to_string())
}

/// Extract og:image URL.
fn extract_og_image(document: &Html) -> Option<String> {
    let sel = Selector::parse("meta[property='og:image']").ok()?;
    document
        .select(&sel)
        .next()
        .and_then(|el| el.value().attr("content"))
        .map(|s| s.to_string())
}

/// Extract bathrooms from meta description like "5 beds, 3 baths".
fn extract_baths_from_meta(document: &Html) -> Option<i64> {
    let sel = Selector::parse("meta[name='description']").ok()?;
    let desc = document
        .select(&sel)
        .next()
        .and_then(|el| el.value().attr("content"))?;
    let re = Regex::new(r"(\d+)\s*baths?").ok()?;
    re.captures(desc)
        .and_then(|c| c.get(1))
        .and_then(|m| m.as_str().parse().ok())
}

// ── Main parse function ──────────────────────────────────────────────────────

pub fn parse(url: &str, html: &str) -> Option<ParsedListing> {
    if html.len() < 5000 {
        return None;
    }

    let document = Html::parse_document(html);
    let json_ld = extract_json_ld(&document);
    let ld = extract_from_json_ld(&json_ld);
    let next = extract_next_data(html);

    let beds = ld.beds;
    let baths = next.baths.or_else(|| extract_baths_from_meta(&document));
    let mls = next
        .mls_number
        .or_else(|| extract_mls_from_title(&document));

    // Build title.
    let title = match (&ld.street_address, &ld.city, beds, baths) {
        (Some(street), Some(city), Some(b), Some(ba)) => {
            format!("{street}, {city} - {b} beds/{ba} baths")
        }
        (Some(street), Some(city), _, _) => format!("{street}, {city}"),
        _ => String::new(),
    };

    // Collect images: prefer __NEXT_DATA__, fall back to og:image.
    let mut image_urls = next.images;
    if image_urls.is_empty() {
        if let Some(og) = extract_og_image(&document) {
            image_urls.push(og);
        }
    }

    // Bail if we got nothing useful.
    if ld.price.is_none() && beds.is_none() && ld.street_address.is_none() {
        return None;
    }

    Some(ParsedListing {
        property: StoredProperty {
            id: 0,
            search_profile_id: None, // overwritten by caller
            title,
            description: next.description.unwrap_or_default(),
            price: ld.price,
            price_currency: ld.currency,
            offer_price: None,
            street_address: ld.street_address,
            city: ld.city,
            region: ld.region,
            postal_code: ld.postal_code,
            country: Some("CA".to_string()),
            lat: ld.lat,
            lon: ld.lon,
            bedrooms: beds,
            bathrooms: baths,
            sqft: ld.sqft,
            year_built: next.year_built,
            land_sqft: next.lot_sqft,
            property_type: next.property_type,
            parking_total: next.parking_total,
            parking_garage: None,
            parking_carport: None,
            parking_pad: None,
            property_tax: next.property_tax,
            hoa_monthly: next.hoa_monthly,
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
            listed_date: next.listed_date,
            status: crate::models::property::ListingStatus::Interested,
            redfin_url: None,
            realtor_url: None,
            rew_url: None,
            zillow_url: Some(url.to_string()),
            notes: None,
            created_at: String::new(),
            updated_at: None,
        },
        image_urls,
        open_houses: vec![],
    })
}

// ── Tests ────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsers::test_support::{fixture, listing_to_property};

    #[test]
    fn zillow_3545_w_king_edward() {
        let html =
            std::fs::read_to_string(fixture("zillow_3545_w_king_edward.html")).unwrap();
        let listing = parse(
            "https://www.zillow.com/homedetails/3545-King-Edward-Ave-W-Vancouver-BC-V6S-1M4/460652473_zpid/",
            &html,
        )
        .expect("should parse zillow listing");
        let prop = listing_to_property(listing);
        insta::assert_json_snapshot!(prop);
    }
}
