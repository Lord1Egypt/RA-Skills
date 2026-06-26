//! URL parsing and canonicalization for listing sources.

use url::Url;

/// A validated HTTP/HTTPS URL for a known listing site.
pub(crate) struct ListingUrl {
    pub(crate) url: Url,
    pub(crate) site: crate::parsers::ListingSite,
}

/// Parse and validate `input` as an HTTP/HTTPS URL from a known listing site.
/// Strips query parameters to produce a canonical URL suitable for deduplication.
/// Returns `None` for malformed strings, non-HTTP schemes, or unrecognised hosts.
pub(crate) fn parse_listing_url(input: &str) -> Option<ListingUrl> {
    let cleaned = strip_url_query(input);
    let u = Url::parse(&cleaned).ok()?;
    match u.scheme() {
        "http" | "https" => {
            let site = crate::parsers::ListingSite::from_url(&cleaned)?;
            Some(ListingUrl { url: u, site })
        }
        _ => None,
    }
}

/// Strip query parameters from a URL string, returning the cleaned URL.
/// If the input cannot be parsed as a URL, returns it unchanged.
pub(crate) fn strip_url_query(url: &str) -> String {
    Url::parse(url)
        .ok()
        .map(|mut u| {
            u.set_query(None);
            u.to_string()
        })
        .unwrap_or_else(|| url.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsers::ListingSite;

    #[test]
    fn accepts_known_https_url() {
        let lu = parse_listing_url("https://www.redfin.com/home/123").unwrap();
        assert_eq!(lu.url.scheme(), "https");
        assert_eq!(lu.site, ListingSite::Redfin);
    }

    #[test]
    fn detects_all_listing_sites() {
        assert_eq!(parse_listing_url("https://www.redfin.com/h").unwrap().site, ListingSite::Redfin);
        assert_eq!(parse_listing_url("https://www.rew.ca/p").unwrap().site, ListingSite::Rew);
        assert_eq!(parse_listing_url("https://www.zillow.com/h").unwrap().site, ListingSite::Zillow);
        assert_eq!(parse_listing_url("https://www.realtor.ca/h").unwrap().site, ListingSite::Realtor);
    }

    #[test]
    fn strips_query_string() {
        let lu = parse_listing_url("https://redfin.com/home?ref=email&utm_source=foo").unwrap();
        assert_eq!(lu.url.query(), None);
        assert_eq!(lu.url.path(), "/home");
    }

    #[test]
    fn rejects_unknown_site() {
        assert!(parse_listing_url("https://example.com/listing").is_none());
    }

    #[test]
    fn rejects_ftp() {
        assert!(parse_listing_url("ftp://example.com/file").is_none());
    }

    #[test]
    fn rejects_javascript_scheme() {
        assert!(parse_listing_url("javascript:alert(1)").is_none());
    }

    #[test]
    fn rejects_bare_string() {
        assert!(parse_listing_url("not a url").is_none());
    }

    #[test]
    fn rejects_empty_string() {
        assert!(parse_listing_url("").is_none());
    }
}
