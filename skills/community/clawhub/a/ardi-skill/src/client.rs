// HTTP client to the Ardi coordinator server (coord-rs).

use anyhow::{anyhow, Context, Result};
use reqwest::blocking::Client;
use serde::de::DeserializeOwned;
use serde_json::Value;
use std::time::Duration;

pub struct ApiClient {
    base: String,
    http: Client,
}

impl ApiClient {
    pub fn new(base: impl Into<String>) -> Result<Self> {
        let http = Client::builder()
            .timeout(Duration::from_secs(15))
            .user_agent(concat!("ardi-agent/", env!("CARGO_PKG_VERSION")))
            .build()?;
        Ok(Self {
            base: base.into().trim_end_matches('/').to_string(),
            http,
        })
    }

    pub fn base(&self) -> &str {
        &self.base
    }

    /// GET with internal retry. coord-rs sits behind nginx + a long-running
    /// process; restarts and brief TLS handshake EOFs do happen
    /// (reproduced 2026-05-03 by a tester whose `inscribe` poll loop
    /// died on a single transient TLS error). 3 attempts with 1s/2s
    /// backoff covers a coord watchdog restart (~3s downtime) without
    /// surfacing the blip to the LLM as a hard failure.
    fn get_with_retry(&self, path: &str) -> Result<reqwest::blocking::Response> {
        let url = format!("{}{}", self.base, path);
        let mut last_err: Option<anyhow::Error> = None;
        for attempt in 0..3 {
            if attempt > 0 {
                std::thread::sleep(Duration::from_secs(1u64 << (attempt - 1))); // 1s, 2s
            }
            match self.http.get(&url).send() {
                Ok(r) => {
                    // Retry on transient 5xx; 4xx is the caller's fault.
                    let s = r.status().as_u16();
                    if s >= 500 && s < 600 && attempt < 2 {
                        last_err = Some(anyhow!("HTTP {s} from {url} (attempt {})", attempt + 1));
                        continue;
                    }
                    return Ok(r);
                }
                Err(e) => {
                    last_err = Some(anyhow!("GET {url} (attempt {}): {e}", attempt + 1));
                    continue;
                }
            }
        }
        Err(last_err.unwrap_or_else(|| anyhow!("GET {url}: 3 attempts failed")))
    }

    pub fn get_json<T: DeserializeOwned>(&self, path: &str) -> Result<T> {
        let url = format!("{}{}", self.base, path);
        let resp = self.get_with_retry(path)?;
        let status = resp.status();
        let text = resp.text().unwrap_or_default();
        if !status.is_success() {
            return Err(anyhow!("HTTP {} from {}: {}", status.as_u16(), url, text));
        }
        serde_json::from_str(&text)
            .with_context(|| format!("parse JSON from {url}: {text}"))
    }

    pub fn try_get_json<T: DeserializeOwned>(&self, path: &str) -> Result<Option<T>> {
        let url = format!("{}{}", self.base, path);
        let resp = self.get_with_retry(path)?;
        if resp.status().as_u16() == 404 {
            return Ok(None);
        }
        let status = resp.status();
        let text = resp.text().unwrap_or_default();
        if !status.is_success() {
            return Err(anyhow!("HTTP {} from {}: {}", status.as_u16(), url, text));
        }
        let v = serde_json::from_str(&text)
            .with_context(|| format!("parse JSON from {url}: {text}"))?;
        Ok(Some(v))
    }

    pub fn ping(&self) -> Result<Value> {
        self.get_json("/v1/health")
    }
}
