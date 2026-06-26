//! Refresh all listings via the AgentZero API.
//!
//! For each listing, fetches a live preview of the refreshed data, shows what
//! would change, then asks for confirmation (unless --auto-accept is set).
//!
//! Usage:
//!   cargo run --bin refresh_all
//!   cargo run --bin refresh_all -- --id 41
//!   cargo run --bin refresh_all -- --status Interested,Buyable
//!   cargo run --bin refresh_all -- --auto-accept
//!   cargo run --bin refresh_all -- --dry-run
//!
//! Reads BACKEND_PORT from the environment (default: 8000).

use agent_zero_backend::api::refresh::ResolvedListing;
use agent_zero_backend::models::open_house::OpenHouse;
use clap::Parser;
use serde::Deserialize;
use std::env;
use std::io::{self, BufRead, Write};

const DEFAULT_PORT: u16 = 8000;
const DEFAULT_FRONTEND_PORT: u16 = 5173;

/// Refresh all listings from their source URLs.
#[derive(Parser)]
#[command(name = "refresh_all")]
struct Cli {
    /// Refresh a single listing by ID instead of all listings.
    #[arg(long, value_name = "ID")]
    id: Option<i64>,

    /// Only refresh listings with these statuses (comma-separated).
    /// Valid values: Interested, Buyable, HumanReview, AgentPending, AgentSkip, Pass
    #[arg(long, value_name = "STATUS,...")]
    status: Option<String>,

    /// Refresh all listings without per-listing confirmation prompts
    #[arg(long)]
    auto_accept: bool,

    /// Show what would change without actually refreshing
    #[arg(long)]
    dry_run: bool,
}

#[derive(Deserialize, Clone)]
struct Listing {
    id: i64,
    title: String,
    status: String,
    source_status: Option<String>,
    price: Option<i64>,
    price_currency: Option<String>,
    street_address: Option<String>,
    bedrooms: Option<i64>,
    bathrooms: Option<i64>,
    property_tax: Option<i64>,
    hoa_monthly: Option<i64>,
    listed_date: Option<String>,
    mls_number: Option<String>,
    redfin_url: Option<String>,
    realtor_url: Option<String>,
    rew_url: Option<String>,
    zillow_url: Option<String>,
    #[serde(default)]
    open_houses: Vec<OpenHouse>,
}

// ── ANSI ────────────────────────────────────────────────────────────────────

const BOLD:   &str = "\x1b[1m";
const DIM:    &str = "\x1b[2m";
const RESET:  &str = "\x1b[0m";
const GREEN:  &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const RED:    &str = "\x1b[31m";
const CYAN:   &str = "\x1b[36m";

fn fmt_review_status(s: &str) -> String {
    match s {
        "Buyable"      => format!("{GREEN}{BOLD}{s}{RESET}"),
        "Interested"   => format!("{CYAN}{s}{RESET}"),
        "HumanReview"  => format!("{YELLOW}Review{RESET}"),
        "AgentPending" => format!("{DIM}{CYAN}Analyzing…{RESET}"),
        "AgentSkip"    => format!("{DIM}Skipped{RESET}"),
        "Pass"         => format!("{DIM}{s}{RESET}"),
        _              => s.to_string(),
    }
}

fn fmt_source_status(s: Option<&str>) -> String {
    match s {
        None => format!("{GREEN}Active{RESET}"),
        Some(v) if v.eq_ignore_ascii_case("pending") => format!("{YELLOW}{v}{RESET}"),
        Some(v) => format!("{RED}{v}{RESET}"),
    }
}

struct Change {
    label: &'static str,
    from: String,
    to: String,
}

fn fmt_dollars(cents: &i64) -> String {
    let n = *cents as u64;
    let s = n.to_string();
    let mut out = String::with_capacity(s.len() + s.len() / 3 + 1);
    for (i, ch) in s.chars().rev().enumerate() {
        if i > 0 && i % 3 == 0 {
            out.push(',');
        }
        out.push(ch);
    }
    format!("${}", out.chars().rev().collect::<String>())
}

fn fmt_open_houses(open_houses: &[OpenHouse]) -> String {
    if open_houses.is_empty() {
        return "—".to_string();
    }
    open_houses
        .iter()
        .map(|oh| {
            // Parse ISO datetime "2026-03-22T14:00:00" → "2026-03-22 2:00 PM"
            let date_part = oh.start_time.get(..10).unwrap_or(&oh.start_time);
            let time_part = oh.start_time.get(11..16).unwrap_or("");
            let end_part = oh
                .end_time
                .as_deref()
                .and_then(|e| e.get(11..16))
                .map(|t| format!("–{t}"))
                .unwrap_or_default();
            format!("{date_part} {time_part}{end_part}")
        })
        .collect::<Vec<_>>()
        .join(", ")
}

fn fmt_opt_str(v: &Option<String>) -> String {
    v.as_deref().unwrap_or("—").to_string()
}

fn fmt_opt_i64(v: &Option<i64>) -> String {
    v.map(|n| n.to_string()).unwrap_or_else(|| "—".to_string())
}

fn compute_diff(current: &Listing, preview: &Listing) -> Vec<Change> {
    let mut changes = Vec::new();

    macro_rules! field {
        ($label:expr, $field:ident, $fmt:expr) => {
            if current.$field != preview.$field {
                changes.push(Change {
                    label: $label,
                    from: $fmt(&current.$field),
                    to: $fmt(&preview.$field),
                });
            }
        };
    }

    // title is non-optional
    if current.title != preview.title {
        changes.push(Change {
            label: "title",
            from: current.title.clone(),
            to: preview.title.clone(),
        });
    }

    field!("street_address", street_address, fmt_opt_str);
    field!("price_currency", price_currency, fmt_opt_str);

    if current.price != preview.price {
        changes.push(Change {
            label: "price",
            from: current.price.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
            to: preview.price.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
        });
    }

    field!("bedrooms", bedrooms, fmt_opt_i64);
    field!("bathrooms", bathrooms, fmt_opt_i64);

    if current.property_tax != preview.property_tax {
        changes.push(Change {
            label: "property_tax",
            from: current.property_tax.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
            to: preview.property_tax.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
        });
    }

    if current.hoa_monthly != preview.hoa_monthly {
        changes.push(Change {
            label: "hoa_monthly",
            from: current.hoa_monthly.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
            to: preview.hoa_monthly.as_ref().map(fmt_dollars).unwrap_or_else(|| "—".to_string()),
        });
    }

    field!("listed_date", listed_date, fmt_opt_str);
    field!("mls_number", mls_number, fmt_opt_str);
    field!("property status", source_status, fmt_opt_str);

    // Open houses are additive-only — refresh never removes existing entries.
    // Only show newly parsed ones that aren't already stored.
    let current_times: std::collections::HashSet<&str> =
        current.open_houses.iter().map(|oh| oh.start_time.as_str()).collect();
    let new_open_houses: Vec<&OpenHouse> = preview
        .open_houses
        .iter()
        .filter(|oh| !current_times.contains(oh.start_time.as_str()))
        .collect();
    if !new_open_houses.is_empty() {
        let new_cloned: Vec<OpenHouse> = new_open_houses.into_iter().cloned().collect();
        changes.push(Change {
            label: "open_houses (new)",
            from: "—".to_string(),
            to: fmt_open_houses(&new_cloned),
        });
    }

    changes
}

fn print_diff(changes: &[Change]) {
    if changes.is_empty() {
        println!("  no changes detected");
        return;
    }
    let label_width = changes.iter().map(|c| c.label.len()).max().unwrap_or(0);
    for c in changes {
        println!("  {:<width$}  {}  →  {}", c.label, c.from, c.to, width = label_width);
    }
}

pub async fn run() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    let port: u16 = env::var("BACKEND_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(DEFAULT_PORT);
    let base_url = format!("http://127.0.0.1:{port}");

    let frontend_port: u16 = env::var("FRONTEND_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(DEFAULT_FRONTEND_PORT);
    let frontend_base_url = format!("http://127.0.0.1:{frontend_port}");

    let client = reqwest::Client::new();

    let listings: Vec<Listing> = if let Some(id) = cli.id {
        let url = format!("{base_url}/api/listings/{id}");
        println!("[refresh-all] fetching listing {id} from {url}...");
        let response = client
            .get(&url)
            .send()
            .await
            .map_err(|e| format!("Failed to reach backend at {base_url}: {e}"))?;
        if !response.status().is_success() {
            return Err(format!("Backend returned {} for listing {id}", response.status()).into());
        }
        vec![response.json::<Listing>().await?]
    } else {
        let listings_url = match &cli.status {
            Some(s) => format!("{base_url}/api/listings?status={s}"),
            None => format!("{base_url}/api/listings"),
        };
        println!("[refresh-all] fetching listings from {listings_url}...");
        let response = client
            .get(&listings_url)
            .send()
            .await
            .map_err(|e| format!("Failed to reach backend at {base_url}: {e}"))?;
        if !response.status().is_success() {
            return Err(format!("Backend returned {}", response.status()).into());
        }
        response.json().await?
    };
    let total = listings.len();

    if total == 0 {
        println!("[refresh-all] no listings found");
        return Ok(());
    }

    println!("[refresh-all] found {total} listing(s)");
    if cli.dry_run {
        println!("[refresh-all] dry-run mode — no changes will be made");
    }

    let mut refreshed = 0u32;
    let mut skipped = 0u32;
    let mut failed = 0u32;

    let stdin = io::stdin();
    let mut stdin_lock = stdin.lock();

    for (index, listing) in listings.iter().enumerate() {
        println!(
            "\n  [{}/{}] #{} 🏠 {BOLD}{}{RESET}",
            index + 1, total, listing.id, listing.title,
        );
        println!("     📋 Review status:   {}", fmt_review_status(&listing.status));
        println!("     🏷  Property status: {}", fmt_source_status(listing.source_status.as_deref()));
        for url in [&listing.redfin_url, &listing.realtor_url, &listing.rew_url, &listing.zillow_url]
            .into_iter().flatten()
        {
            println!("     🔗 {DIM}{url}{RESET}");
        }
        println!("     🌐 {DIM}{frontend_base_url}/property/{}{RESET}", listing.id);

        // Fetch preview to compute diff
        print!("  previewing...");
        io::stdout().flush()?;

        let preview_url = format!("{base_url}/api/listings/{}/preview", listing.id);
        let preview_result = client.get(&preview_url).send().await;

        match preview_result {
            Err(e) => {
                println!(" FAILED: {e}");
                if !cli.auto_accept && !cli.dry_run {
                    print!("  Refresh anyway? [y/N] ");
                    io::stdout().flush()?;
                    let mut line = String::new();
                    stdin_lock.read_line(&mut line)?;
                    if !matches!(line.trim(), "y" | "Y") {
                        println!("  skipped");
                        skipped += 1;
                        continue;
                    }
                } else if cli.dry_run {
                    continue;
                }
            }
            Ok(resp) if !resp.status().is_success() => {
                let status = resp.status().as_u16();
                let body = resp.text().await.unwrap_or_default();
                println!(" FAILED (HTTP {status}): {body}");
                skipped += 1;
                continue;
            }
            Ok(resp) => {
                println!();
                let has_changes = match resp.json::<ResolvedListing>().await {
                    Ok(ResolvedListing::StatusOnly { source_status }) => {
                        let from = listing.source_status.as_deref().unwrap_or("—");
                        let to = source_status.to_string();
                        let changed = listing.source_status.as_deref() != Some(to.as_str());
                        if changed {
                            println!("  [status-only]  property status  {}  →  {}", from, to);
                        } else {
                            println!("  no changes detected");
                        }
                        changed
                    }
                    Ok(ResolvedListing::Full { property }) => {
                        let preview = Listing {
                            id: property.id,
                            title: property.title,
                            status: property.status.to_string(),
                            source_status: property.source_status.map(|s| s.to_string()),
                            price: property.price,
                            price_currency: property.price_currency,
                            street_address: property.street_address,
                            bedrooms: property.bedrooms,
                            bathrooms: property.bathrooms,
                            property_tax: property.property_tax,
                            hoa_monthly: property.hoa_monthly,
                            listed_date: property.listed_date,
                            mls_number: property.mls_number,
                            redfin_url: property.redfin_url,
                            realtor_url: property.realtor_url,
                            rew_url: property.rew_url,
                            zillow_url: property.zillow_url,
                            open_houses: property.open_houses,
                        };
                        let changes = compute_diff(listing, &preview);
                        print_diff(&changes);
                        !changes.is_empty()
                    }
                    Err(e) => {
                        println!("  (could not parse preview: {e})");
                        true // assume changes if we couldn't diff
                    }
                };

                if !has_changes {
                    println!("  skipped");
                    skipped += 1;
                    continue;
                }

                if cli.dry_run {
                    continue;
                }

                if !cli.auto_accept {
                    print!("  Refresh? [y/N] ");
                    io::stdout().flush()?;
                    let mut line = String::new();
                    stdin_lock.read_line(&mut line)?;
                    if !matches!(line.trim(), "y" | "Y") {
                        println!("  skipped");
                        skipped += 1;
                        continue;
                    }
                }
            }
        }

        let refresh_url = format!("{base_url}/api/listings/{}/refresh", listing.id);
        match client.put(&refresh_url).send().await {
            Ok(resp) if resp.status().is_success() => {
                println!("  refreshed (HTTP {})", resp.status().as_u16());
                refreshed += 1;
            }
            Ok(resp) => {
                let status = resp.status().as_u16();
                let body = resp.text().await.unwrap_or_default();
                eprintln!("  FAILED (HTTP {status}): {body}");
                failed += 1;
            }
            Err(e) => {
                eprintln!("  FAILED: {e}");
                failed += 1;
            }
        }
    }

    println!();
    if cli.dry_run {
        println!("[refresh-all] dry-run complete — {total} listing(s) previewed");
    } else {
        println!("[refresh-all] done — refreshed={refreshed} skipped={skipped} failed={failed}");
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Build a `Listing` with all fields listed explicitly — intentionally no `..`.
    ///
    /// This is the enforcement mechanism: adding a new field to `Listing` causes a
    /// compile error here, which forces every new field to be consciously added to
    /// `compute_diff` or added to `SKIPPED_FIELDS` with a documented reason.
    fn make_listing(variant: u8) -> Listing {
        if variant == 0 {
            Listing {
                id: 1,                                                    // skipped: identity
                title: "Before Title".to_string(),
                status: "Interested".to_string(),                         // skipped: user-owned
                source_status: None,
                price: Some(500_000),
                price_currency: Some("CAD".to_string()),
                street_address: Some("123 Before St".to_string()),
                bedrooms: Some(2),
                bathrooms: Some(1),
                property_tax: Some(3_000),
                hoa_monthly: Some(200),
                listed_date: Some("2026-01-01".to_string()),
                mls_number: Some("R1111111".to_string()),
                redfin_url: Some("https://redfin.ca/1".to_string()),      // skipped: display-only
                realtor_url: None,                                        // skipped: display-only
                rew_url: None,                                            // skipped: display-only
                zillow_url: None,                                         // skipped: display-only
                open_houses: vec![],
            }
        } else {
            Listing {
                id: 1,                                                    // skipped: identity
                title: "After Title".to_string(),
                status: "Pass".to_string(),                               // skipped: user-owned
                source_status: Some("OffMarket".to_string()),
                price: Some(550_000),
                price_currency: Some("USD".to_string()),
                street_address: Some("456 After Ave".to_string()),
                bedrooms: Some(3),
                bathrooms: Some(2),
                property_tax: Some(4_000),
                hoa_monthly: Some(300),
                listed_date: Some("2026-06-01".to_string()),
                mls_number: Some("R2222222".to_string()),
                redfin_url: Some("https://redfin.ca/2".to_string()),      // skipped: display-only
                realtor_url: None,                                        // skipped: display-only
                rew_url: None,                                            // skipped: display-only
                zillow_url: None,                                         // skipped: display-only
                open_houses: vec![OpenHouse {
                    id: -1,
                    listing_id: 1,
                    start_time: "2026-06-15T14:00:00".to_string(),
                    end_time: Some("2026-06-15T16:00:00".to_string()),
                    visited: false,
                    created_at: String::new(),
                }],
            }
        }
    }

    /// Fields intentionally excluded from `compute_diff` with documented reasons.
    /// When a new field is added to `Listing`:
    ///   - add it to `compute_diff`, OR
    ///   - add it here with a reason.
    const SKIPPED_FIELDS: &[&str] = &[
        "id",          // identity — not a content change
        "status",      // user-owned — not sourced from the listing page
        "redfin_url",  // display-only — user-managed, not refreshed from page
        "realtor_url", // display-only — user-managed, not refreshed from page
        "rew_url",     // display-only — user-managed, not refreshed from page
        "zillow_url",  // display-only — user-managed, not refreshed from page
    ];

    /// Verify that every non-skipped field in `Listing` produces a diff entry
    /// when it changes. The count assertion fails if a field was added to the
    /// struct but not added to `compute_diff` or `SKIPPED_FIELDS`.
    #[test]
    fn test_compute_diff_covers_all_listing_fields() {
        let before = make_listing(0);
        let after = make_listing(1);
        let changes = compute_diff(&before, &after);

        // Count must equal: total Listing fields − skipped fields.
        // Update this number whenever a field is added or removed from Listing.
        //
        // Current Listing fields (18):
        //   id, title, status, source_status, price, price_currency,
        //   street_address, bedrooms, bathrooms, property_tax, hoa_monthly,
        //   listed_date, mls_number, redfin_url, realtor_url, rew_url, zillow_url, open_houses
        const TOTAL_LISTING_FIELDS: usize = 18;
        let expected = TOTAL_LISTING_FIELDS - SKIPPED_FIELDS.len();

        assert_eq!(
            changes.len(),
            expected,
            "compute_diff detected {} change(s) but expected {}. \
             If you added a field to Listing, either add it to compute_diff \
             or add it to SKIPPED_FIELDS with a reason.",
            changes.len(),
            expected,
        );
    }

    #[test]
    fn test_compute_diff_no_changes_when_equal() {
        let listing = make_listing(0);
        let changes = compute_diff(&listing, &listing.clone());
        assert!(changes.is_empty(), "expected no changes for identical listings");
    }
}
