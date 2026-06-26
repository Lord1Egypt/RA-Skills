// RPC pool — round-robin over public Base mainnet endpoints, with
// ChainList.org as a runtime fallback so we keep working even when our
// hardcoded list goes stale. NEVER points at our paid RPC; agents bring
// their own (or use the public list below).
//
// Override priority:
//   1. ARDI_BASE_RPC env (single URL or comma-separated list)
//   2. Hardcoded public list (good defaults, no key needed)
//   3. ChainList.org fetch (lazy, cached for 1 hour)

use anyhow::{anyhow, Context, Result};
use reqwest::blocking::Client;
use serde_json::{json, Value};
use std::sync::Mutex;
use std::time::{Duration, Instant};

/// Hardcoded public Base mainnet RPCs, no API key required. Order is
/// the initial round-robin sequence; on failure we rotate to the next.
const PUBLIC_RPCS: &[&str] = &[
    "https://mainnet.base.org",
    "https://base-rpc.publicnode.com",
    "https://base.drpc.org",
    "https://base.llamarpc.com",
    "https://base.meowrpc.com",
    "https://1rpc.io/base",
    "https://base-mainnet.public.blastapi.io",
];

/// Cached ChainList result.
struct ChainListCache {
    fetched_at: Instant,
    rpcs: Vec<String>,
}

static CACHE: Mutex<Option<ChainListCache>> = Mutex::new(None);
static CURSOR: Mutex<usize> = Mutex::new(0);

fn http() -> Client {
    Client::builder()
        .timeout(Duration::from_secs(8))
        .build()
        .expect("reqwest client")
}

/// Resolve the ordered RPC list for this run.
fn rpc_list() -> Vec<String> {
    if let Ok(env) = std::env::var("ARDI_BASE_RPC") {
        let v: Vec<String> = env
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();
        if !v.is_empty() {
            return v;
        }
    }
    PUBLIC_RPCS.iter().map(|s| s.to_string()).collect()
}

/// Pull RPCs from chainlist.org (cached 1h). Used when the static list
/// has all-failed in this process. Filtered to chainId=8453, excludes
/// known-key-required URLs.
fn chainlist_extra() -> Vec<String> {
    {
        let g = CACHE.lock().unwrap();
        if let Some(c) = g.as_ref() {
            if c.fetched_at.elapsed() < Duration::from_secs(3600) {
                return c.rpcs.clone();
            }
        }
    }

    let url = "https://chainlist.org/rpcs.json";
    let resp: Result<Value> = http()
        .get(url)
        .send()
        .context("chainlist GET")
        .and_then(|r| r.json().context("chainlist JSON"));
    let v = match resp {
        Ok(v) => v,
        Err(_) => return Vec::new(),
    };

    let mut rpcs: Vec<String> = Vec::new();
    if let Some(arr) = v.as_array() {
        for chain in arr {
            if chain.get("chainId").and_then(|x| x.as_u64()) != Some(8453) {
                continue;
            }
            if let Some(list) = chain.get("rpc").and_then(|r| r.as_array()) {
                for entry in list {
                    let url = entry
                        .get("url")
                        .and_then(|u| u.as_str())
                        .unwrap_or_default();
                    if url.is_empty() || url.starts_with("ws") {
                        continue;
                    }
                    // Skip URLs that need API keys (e.g. ${...} templating).
                    if url.contains("${") || url.contains("API_KEY") {
                        continue;
                    }
                    rpcs.push(url.to_string());
                }
            }
        }
    }

    if !rpcs.is_empty() {
        let mut g = CACHE.lock().unwrap();
        *g = Some(ChainListCache {
            fetched_at: Instant::now(),
            rpcs: rpcs.clone(),
        });
    }
    rpcs
}

fn next_cursor() -> usize {
    let mut g = CURSOR.lock().unwrap();
    let v = *g;
    *g = (*g + 1) % usize::MAX;
    v
}

/// Send a JSON-RPC request, rotating RPCs on failure. Returns the
/// `result` field on success.
pub fn call(method: &str, params: Value) -> Result<Value> {
    let mut all = rpc_list();
    let req = json!({ "jsonrpc": "2.0", "method": method, "params": params, "id": 1 });
    let mut last_err: Option<String> = None;

    let try_one = |url: &str, last_err: &mut Option<String>| -> Option<Value> {
        match http().post(url).json(&req).send() {
            Ok(resp) => match resp.json::<Value>() {
                Ok(v) => {
                    if let Some(e) = v.get("error") {
                        *last_err = Some(format!("{url}: rpc error {e}"));
                        None
                    } else {
                        Some(v.get("result").cloned().unwrap_or(Value::Null))
                    }
                }
                Err(e) => {
                    *last_err = Some(format!("{url}: parse {e}"));
                    None
                }
            },
            Err(e) => {
                *last_err = Some(format!("{url}: send {e}"));
                None
            }
        }
    };

    // First pass: hardcoded list, starting from rotating cursor.
    let start = next_cursor() % all.len().max(1);
    for i in 0..all.len() {
        let idx = (start + i) % all.len();
        if let Some(v) = try_one(&all[idx], &mut last_err) {
            return Ok(v);
        }
    }

    // Second pass: try ChainList live list (lazy + cached).
    let extra = chainlist_extra();
    if !extra.is_empty() {
        for url in &extra {
            if all.contains(url) {
                continue;
            }
            if let Some(v) = try_one(url, &mut last_err) {
                all.push(url.clone());
                return Ok(v);
            }
        }
    }

    Err(anyhow!(
        "all Base RPCs failed (tried {} hardcoded + {} from chainlist). Last: {}",
        all.len(),
        extra.len(),
        last_err.unwrap_or_else(|| "no error captured".into())
    ))
}
