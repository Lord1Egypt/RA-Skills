//! Trigger and inspect agent review for listings.
//!
//! Usage:
//!   cargo run --bin agent_review               # review all AgentPending listings
//!   cargo run --bin agent_review -- --id 89    # review a single listing
//!   BACKEND_PORT=8000 cargo run --bin agent_review

use clap::Parser;
use serde::Deserialize;
use std::env;
use std::time::Instant;

const DEFAULT_PORT: u16 = 8000;
const POLL_INTERVAL_MS: u64 = 500;
const TIMEOUT_SECS: u64 = 30;

const BOLD:   &str = "\x1b[1m";
const DIM:    &str = "\x1b[2m";
const RESET:  &str = "\x1b[0m";
const GREEN:  &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const RED:    &str = "\x1b[31m";
const CYAN:   &str = "\x1b[36m";

#[derive(Parser)]
#[command(name = "agent_review")]
struct Cli {
    /// Listing ID to run agent review on. Omit to process all AgentPending listings.
    #[arg(long, value_name = "ID")]
    id: Option<i64>,
}

#[derive(Deserialize, Clone)]
struct Listing {
    id: i64,
    title: String,
    status: String,
    agent_comment: Option<String>,
    search_profile_id: Option<i64>,
}

fn fmt_status(s: &str) -> String {
    match s {
        "Buyable"      => format!("{GREEN}{BOLD}{s}{RESET}"),
        "Interested"   => format!("{CYAN}{s}{RESET}"),
        "HumanReview"  => format!("{YELLOW}HumanReview{RESET}"),
        "AgentPending" => format!("{DIM}AgentPending{RESET}"),
        "AgentSkip"    => format!("{DIM}AgentSkip{RESET}"),
        "Pass"         => format!("{DIM}{s}{RESET}"),
        _              => s.to_string(),
    }
}

pub async fn run() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    let port: u16 = env::var("BACKEND_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(DEFAULT_PORT);
    let base_url = format!("http://127.0.0.1:{port}");

    let client = reqwest::Client::new();

    let ids: Vec<i64> = if let Some(id) = cli.id {
        vec![id]
    } else {
        let listings: Vec<Listing> = client
            .get(format!("{base_url}/api/listings"))
            .send()
            .await
            .map_err(|e| format!("Failed to reach backend at {base_url}: {e}"))?
            .error_for_status()
            .map_err(|e| format!("Failed to fetch listings: {e}"))?
            .json()
            .await?;

        let pending: Vec<i64> = listings.iter()
            .filter(|l| l.status == "AgentPending")
            .map(|l| l.id)
            .collect();

        if pending.is_empty() {
            println!("[agent-review] no AgentPending listings found");
            return Ok(());
        }

        println!("[agent-review] found {} AgentPending listing(s)", pending.len());
        pending
    };

    let total = ids.len();
    let mut failed = 0;

    for (i, id) in ids.iter().enumerate() {
        println!();
        if total > 1 {
            println!("[agent-review] ({}/{total})", i + 1);
        }
        if let Err(e) = review_one(&client, &base_url, *id).await {
            eprintln!("{RED}[agent-review] #{id} failed: {e}{RESET}");
            failed += 1;
        }
    }

    if total > 1 {
        println!();
        println!("[agent-review] done — {}/{total} succeeded", total - failed);
    }

    if failed > 0 {
        std::process::exit(1);
    }

    Ok(())
}

async fn review_one(
    client: &reqwest::Client,
    base_url: &str,
    id: i64,
) -> Result<(), String> {
    let listing_url = format!("{base_url}/api/listings/{id}");

    // ── Fetch current state ────────────────────────────────────────────────────
    let before: Listing = client
        .get(&listing_url)
        .send()
        .await
        .map_err(|e| format!("Failed to reach backend: {e}"))?
        .error_for_status()
        .map_err(|e| format!("Listing #{id} not found: {e}"))?
        .json()
        .await
        .map_err(|e| format!("Failed to parse listing: {e}"))?;

    println!(
        "[agent-review] #{} — {BOLD}{}{RESET}",
        before.id, before.title
    );
    println!(
        "  before: status={} comment={}",
        fmt_status(&before.status),
        before.agent_comment.as_deref()
            .map(|c| format!("{DIM}\"{c}\"{RESET}"))
            .unwrap_or_else(|| format!("{DIM}—{RESET}")),
    );

    // ── Trigger review ─────────────────────────────────────────────────────────
    let trigger_url = format!("{base_url}/api/listings/{id}/agent-review/run");
    println!("[agent-review] triggering…");
    client
        .post(&trigger_url)
        .send()
        .await
        .map_err(|e| format!("Trigger request failed: {e}"))?
        .error_for_status()
        .map_err(|e| format!("Trigger failed: {e}"))?;

    // ── Poll for result ────────────────────────────────────────────────────────
    print!("[agent-review] waiting");
    let start = Instant::now();

    loop {
        tokio::time::sleep(tokio::time::Duration::from_millis(POLL_INTERVAL_MS)).await;
        print!(".");

        let after: Listing = match client.get(&listing_url).send().await {
            Ok(r) if r.status().is_success() => match r.json().await {
                Ok(l) => l,
                Err(_) => continue,
            },
            _ => continue,
        };

        let changed = after.agent_comment != before.agent_comment
            || after.status != before.status;

        if changed {
            let elapsed = start.elapsed().as_secs_f32();
            println!(" done ({elapsed:.1}s)");
            println!(
                "  after:  status={} comment={}",
                fmt_status(&after.status),
                after.agent_comment.as_deref()
                    .map(|c| format!("{BOLD}\"{c}\"{RESET}"))
                    .unwrap_or_else(|| format!("{DIM}—{RESET}")),
            );
            if let Some(pid) = after.search_profile_id {
                println!("          search_profile_id={pid}");
            }
            return Ok(());
        }

        if start.elapsed().as_secs() >= TIMEOUT_SECS {
            println!();
            return Err(format!(
                "timed out after {TIMEOUT_SECS}s — check: grep agent_review /tmp/agent_zero_backend.log | tail -20"
            ));
        }
    }
}
