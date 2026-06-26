// awp_rpc — minimal JSON-RPC 2.0 client for AWP rootnet API (api.awp.sh/v2).
//
// Used to discover which staker(s) are backing an agent, replacing the local
// indexer that we used to run on coord-rs. AWP indexes Allocated events
// across all chains and exposes them via `staking.getAllocationsByAgentSubnet`.
//
// The chain-side AWPAllocator.getAgentStake call remains the source of truth
// at commit time — this RPC is only for *discovery* (which staker address to
// pass to ArdiEpochDraw.commit). If AWP is down or returns stale data, the
// commit just reverts at the chain check; no funds at risk.

use anyhow::{anyhow, Context, Result};
use reqwest::blocking::Client;
use serde::{Deserialize, Deserializer};
use serde_json::{json, Value};
use std::time::Duration;

const DEFAULT_AWP_RPC: &str = "https://api.awp.sh/v2";

pub struct AwpRpc {
    url: String,
    http: Client,
}

/// Deserialize an `amount` field that the AWP API serializes as a JSON
/// number on the wire (e.g. `10000000000000000000000`) — too large for an
/// i64/u64, would overflow JS Number precision, but serde happily decodes
/// it as a string for us. Falls back to accepting an actual JSON string
/// so older AWP versions / mock data still parse.
///
/// Without this fix, serde failed silently on the number form and the
/// caller `if let Ok(rows) = …` swallowed the error → skill discovered
/// zero stakers → reported 0 stake even when KYA had clearly delegated.
fn deser_amount_any<'de, D: Deserializer<'de>>(d: D) -> std::result::Result<String, D::Error> {
    // Requires `arbitrary_precision` on serde_json so Number::to_string()
    // preserves the raw integer text instead of round-tripping through f64
    // (which loses precision above ~2^53). For 1e22-scale wei amounts this
    // matters: without arbitrary_precision, "10000000000000000000000"
    // becomes "1e+22" — silently un-parseable as U256 downstream.
    let v = serde_json::Value::deserialize(d)?;
    match v {
        serde_json::Value::String(s) => Ok(s),
        serde_json::Value::Number(n) => Ok(n.to_string()),
        other => Err(serde::de::Error::custom(format!(
            "amount: expected string or number, got {other:?}"
        ))),
    }
}

#[derive(Debug, Clone, Deserialize)]
pub struct AllocationRow {
    pub chain_id: i64,
    pub user_address: String, // = the staker
    /// AWP API returns this as a JSON number (raw uint), not a string.
    /// Stored here as decimal string for downstream U256 parsing.
    #[serde(deserialize_with = "deser_amount_any")]
    pub amount: String,
    pub frozen: bool,
}

impl AwpRpc {
    pub fn new() -> Result<Self> {
        let url = std::env::var("AWP_RPC_URL").unwrap_or_else(|_| DEFAULT_AWP_RPC.to_string());
        let http = Client::builder()
            .timeout(Duration::from_secs(15))
            .user_agent(concat!("ardi-agent/", env!("CARGO_PKG_VERSION")))
            .build()?;
        Ok(Self { url, http })
    }

    fn call(&self, method: &str, params: Value) -> Result<Value> {
        let body = json!({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
        });
        let resp = self
            .http
            .post(&self.url)
            .header("content-type", "application/json")
            .body(body.to_string())
            .send()
            .with_context(|| format!("POST {} method={method}", self.url))?;
        let status = resp.status();
        let text = resp.text().unwrap_or_default();
        if !status.is_success() {
            return Err(anyhow!("HTTP {} from awp rpc: {text}", status.as_u16()));
        }
        let v: Value = serde_json::from_str(&text)
            .with_context(|| format!("parse awp rpc response: {text}"))?;
        if let Some(err) = v.get("error") {
            return Err(anyhow!("awp rpc error: {err}"));
        }
        v.get("result")
            .cloned()
            .ok_or_else(|| anyhow!("awp rpc missing result: {text}"))
    }

    /// Returns the list of (staker, amount) rows backing an agent in a worknet.
    /// Order is amount-desc per the spec. Cross-chain by default; pass `chain_id`
    /// > 0 to restrict to one chain.
    pub fn allocations_by_agent_worknet(
        &self,
        agent: &str,
        worknet_id: &str,
        chain_id: Option<i64>,
    ) -> Result<Vec<AllocationRow>> {
        let mut params = json!({
            "agent": agent,
            "worknetId": worknet_id,
        });
        if let Some(c) = chain_id {
            params["chainId"] = json!(c);
        }
        let v = self.call("staking.getAllocationsByAgentSubnet", params)?;
        let rows: Vec<AllocationRow> = serde_json::from_value(v)
            .context("decode allocation rows")?;
        Ok(rows)
    }

    /// Aggregate stake on a (agent, worknet) summed across every staker
    /// and every chain. Server-side aggregation — one round trip vs. the
    /// per-staker fan-out of `allocations_by_agent_worknet` + per-row
    /// on-chain `getAgentStake`. Use this as the fast-path eligibility
    /// check; fall back to the discover+probe loop only if this errors.
    /// Returns wei as a decimal string.
    pub fn agent_worknet_stake(&self, agent: &str, worknet_id: &str) -> Result<String> {
        let v = self.call(
            "staking.getAgentWorknetStake",
            json!({ "agent": agent, "worknetId": worknet_id }),
        )?;
        // V2 shape: { amount: "<wei decimal string>" }
        let amount = v
            .get("amount")
            .and_then(|x| x.as_str().map(String::from).or_else(|| x.as_u64().map(|n| n.to_string())))
            .ok_or_else(|| anyhow!("agent_worknet_stake: missing `amount` in {v}"))?;
        Ok(amount)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Regression: AWP rootnet RPC returns `amount` as a JSON number (the raw
    /// uint256 wei). Previous code declared it as `String` only and silently
    /// failed to decode the number form — causing skill `stake` to report 0
    /// even when KYA had clearly delegated. Caught only when an external user
    /// raised "agent says 0 but KYA says 10000 AWP". Pin both forms.
    #[test]
    fn allocation_row_decodes_number_amount() {
        let json_num = r#"{
            "chain_id": 8453,
            "user_address": "0x800d05fd8e251c288e22809b79d31f22ab088555",
            "amount": 10000000000000000000000,
            "frozen": false
        }"#;
        let row: AllocationRow = serde_json::from_str(json_num).unwrap();
        assert_eq!(row.amount, "10000000000000000000000");
        assert_eq!(row.user_address, "0x800d05fd8e251c288e22809b79d31f22ab088555");
        assert_eq!(row.chain_id, 8453);
        assert!(!row.frozen);
    }

    #[test]
    fn allocation_row_still_decodes_string_amount() {
        let json_str = r#"{
            "chain_id": 8453,
            "user_address": "0xabc",
            "amount": "10000000000000000000000",
            "frozen": false
        }"#;
        let row: AllocationRow = serde_json::from_str(json_str).unwrap();
        assert_eq!(row.amount, "10000000000000000000000");
    }
}
