//! Strip saved HTML fixture files down to the parts the parsers need.
//!
//! Removes inline styles, SVG content, large data-URIs, tracking scripts,
//! and other bloat while preserving the elements each parser relies on:
//!
//!   **Realtor.ca**: title, meta tags, JSON-LD blocks, `#MLNumberVal`,
//!   `.listingIconNum` elements, `#propertyDetailsSectionContentSubCon_*`
//!   blocks, and highres CDN image URLs.
//!
//!   **Zillow**: title, meta tags, JSON-LD blocks, `__NEXT_DATA__` script.
//!
//! Usage:
//!   cargo run --bin strip                            # strip all fixture files in-place
//!   cargo run --bin strip -- input.html              # strip single file in-place
//!   cargo run --bin strip -- input.html output.html  # strip to separate output

use regex::Regex;
use std::env;
use std::fs;
use std::path::Path;

const FIXTURES_DIR: &str = "src/parsers/fixtures";

/// Remove `<style>...</style>` blocks.
fn strip_styles(html: &str) -> String {
    let re = Regex::new(r"(?si)<style[^>]*>.*?</style>").unwrap();
    re.replace_all(html, "").to_string()
}

/// Remove `<svg>...</svg>` blocks (often large inline icons).
fn strip_svgs(html: &str) -> String {
    let re = Regex::new(r"(?si)<svg[^>]*>.*?</svg>").unwrap();
    re.replace_all(html, "").to_string()
}

/// Remove `<noscript>...</noscript>` blocks.
fn strip_noscript(html: &str) -> String {
    let re = Regex::new(r"(?si)<noscript[^>]*>.*?</noscript>").unwrap();
    re.replace_all(html, "").to_string()
}

/// Keywords that parsers extract from script blocks via regex on raw HTML.
/// Scripts containing these keywords (or JSON-LD / __NEXT_DATA__) are kept.
/// All other scripts are removed.
const DATA_KEYWORDS: &[&str] = &[
    "lotSize",
    "hoaFee",
    "maintenanceFee",
    "monthlyHoaDues",
    "HOA Dues",
    "Maintenance Fee",
    "propertyTax",
    "taxAnnualAmount",
    "carport",
    "Carport",
    "assignedSchools",
    "nearbySchools",
    "schoolName",
    "greatSchoolsRating",
    "Tax Annual Amount",
];

/// Remove scripts that parsers don't need.
/// Keep: JSON-LD, __NEXT_DATA__, and scripts containing DATA_KEYWORDS.
fn strip_scripts(html: &str) -> String {
    let re = Regex::new(r"(?si)<script[^>]*>.*?</script>").unwrap();
    re.replace_all(html, |caps: &regex::Captures| {
        let full = caps.get(0).unwrap().as_str();
        if full.contains("application/ld+json")
            || full.contains("__NEXT_DATA__")
            || DATA_KEYWORDS.iter().any(|kw| full.contains(kw))
        {
            return full.to_string();
        }
        String::new()
    })
    .to_string()
}

/// Remove inline `style="..."` attributes.
fn strip_inline_styles(html: &str) -> String {
    let re = Regex::new(r#"\s+style="[^"]*""#).unwrap();
    re.replace_all(html, "").to_string()
}

/// Remove data-URI `src="data:..."` attributes (base64-encoded images).
fn strip_data_uris(html: &str) -> String {
    let re = Regex::new(r#"(src|href)="data:[^"]{100,}""#).unwrap();
    re.replace_all(html, r#"$1="""#).to_string()
}

/// Remove `srcset="..."` / `srcSet="..."` attributes.
fn strip_srcsets(html: &str) -> String {
    let re = Regex::new(r#"(?i)\s+srcset="[^"]*""#).unwrap();
    re.replace_all(html, "").to_string()
}

/// Collapse blank lines and leading indentation (but not inline spaces).
fn collapse_whitespace(html: &str) -> String {
    let re = Regex::new(r"\n\s*\n(\s*\n)*").unwrap();
    let html = re.replace_all(html, "\n").to_string();
    // Collapse leading whitespace on each line to a single space.
    let re = Regex::new(r"(?m)^[ \t]{2,}").unwrap();
    re.replace_all(&html, " ").to_string()
}

/// Remove HTML comments.
fn strip_comments(html: &str) -> String {
    let re = Regex::new(r"(?s)<!--.*?-->").unwrap();
    re.replace_all(html, "").to_string()
}

/// Remove empty data-* attributes left over after stripping.
fn strip_empty_attrs(html: &str) -> String {
    let re = Regex::new(r#"\s+data-[\w-]+="""#).unwrap();
    re.replace_all(html, "").to_string()
}

fn strip_html(html: &str) -> String {
    let html = strip_comments(html);
    let html = strip_styles(&html);
    let html = strip_svgs(&html);
    let html = strip_noscript(&html);
    let html = strip_scripts(&html);
    let html = strip_inline_styles(&html);
    let html = strip_data_uris(&html);
    let html = strip_srcsets(&html);
    let html = strip_empty_attrs(&html);
    collapse_whitespace(&html)
}

fn strip_file(src: &Path, dst: &Path) {
    let html = fs::read_to_string(src).expect("failed to read input file");
    let original_size = html.len();

    let html = strip_html(&html);

    fs::write(dst, &html).expect("failed to write output file");
    let new_size = html.len();

    let pct = 100.0 * (1.0 - new_size as f64 / original_size as f64);
    eprintln!(
        "{:>10} -> {:>10} ({:.0}% smaller)  {}",
        format_size(original_size),
        format_size(new_size),
        pct,
        dst.display()
    );
}

fn format_size(bytes: usize) -> String {
    if bytes >= 1024 * 1024 {
        format!("{:.1} MB", bytes as f64 / (1024.0 * 1024.0))
    } else if bytes >= 1024 {
        format!("{:.0} KB", bytes as f64 / 1024.0)
    } else {
        format!("{} B", bytes)
    }
}

pub fn run() {
    let args: Vec<String> = env::args().collect();

    if args.len() >= 3 {
        strip_file(Path::new(&args[1]), Path::new(&args[2]));
    } else if args.len() == 2 {
        let src = Path::new(&args[1]);
        strip_file(src, src);
    } else {
        // Default: strip all fixture HTML files in-place.
        let dir = Path::new(FIXTURES_DIR);
        let entries: Vec<_> = fs::read_dir(dir)
            .expect("cannot read fixtures dir")
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().is_some_and(|ext| ext == "html"))
            .collect();

        if entries.is_empty() {
            eprintln!("no .html files found in {}", dir.display());
            return;
        }
        for entry in entries {
            let path = entry.path();
            strip_file(&path, &path);
        }
    }
}
