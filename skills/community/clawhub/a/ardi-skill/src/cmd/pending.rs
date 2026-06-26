// pending — view-only: how much $ardi can the agent claim right now?
//
// Workflow this powers:
//   1. operator asks the LLM agent "how much can I claim today?"
//   2. agent runs `ardi-agent pending`
//   3. skill reports per-NFT pending + total, no tx sent
//   4. operator says "claim", agent runs `ardi-agent claim`
//
// Pulls the agent's owned tokenIds from the coord (`/v1/agent/.../state`),
// then queries EmissionDistributor.pendingFor against the user's own RPC
// (never our paid one — see rpc.rs).

use anyhow::{anyhow, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::{json, Value};
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::EmissionDistributor;
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::tx;
use crate::log_info;

pub fn run(server_url: &str) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;
    let api = ApiClient::new(server_url)?;

    // 1. Owned tokenIds from coord. Coord is the source of truth for
    //    "what NFTs does this agent have"; ardi-view drives the same
    //    state, but state endpoint is the canonical agent view.
    let state: Option<Value> = api
        .try_get_json(&format!("/v1/agent/{agent_str}/state"))
        .unwrap_or(None);
    let token_ids: Vec<u64> = state
        .as_ref()
        .and_then(|v| v.get("mints").and_then(|m| m.as_array()))
        .map(|arr| {
            arr.iter()
                .filter_map(|m| m.get("token_id").and_then(|v| v.as_u64()))
                .collect()
        })
        .unwrap_or_default();

    // 2. Distributor address from coord. Same lookup as claim.rs.
    let cfg: Value = api
        .get_json("/v1/chain/contracts")
        .or_else(|_| api.get_json("/v1/health"))
        .unwrap_or_default();
    let dist_addr = read_addr(&cfg, "emission_distributor")
        .or_else(|| std::env::var("EMISSION_DISTRIBUTOR_ADDR").ok())
        .ok_or_else(|| {
            anyhow!("server didn't return emission_distributor; set EMISSION_DISTRIBUTOR_ADDR")
        })?;
    let dist_addr = Address::from_str(&dist_addr)?;

    // 3. Total pending across all owned NFTs. Single batch view call.
    let token_ids_u: Vec<U256> = token_ids.iter().map(|&t| U256::from(t)).collect();
    let total = if token_ids_u.is_empty() {
        U256::ZERO
    } else {
        let raw = tx::view_call(
            &dist_addr,
            EmissionDistributor::pendingForCall {
                holder: agent,
                tokenIds: token_ids_u.clone(),
            }
            .abi_encode(),
        )?;
        EmissionDistributor::pendingForCall::abi_decode_returns(&raw, true)?._0
    };

    // 4. Per-NFT breakdown so the LLM can show "tid 4 has X, tid 1274 has Y".
    //    Single tokenId per call; loops are fine (≤ a handful of NFTs).
    let mut breakdown: Vec<Value> = Vec::with_capacity(token_ids.len());
    for &tid in &token_ids {
        let raw = tx::view_call(
            &dist_addr,
            EmissionDistributor::pendingForCall {
                holder: agent,
                tokenIds: vec![U256::from(tid)],
            }
            .abi_encode(),
        )?;
        let p = EmissionDistributor::pendingForCall::abi_decode_returns(&raw, true)?._0;
        breakdown.push(json!({
            "token_id": tid,
            "pending_wei": p.to_string(),
            "pending_ardi": format_ardi(p),
        }));
    }

    log_info!(
        "pending: total={} ardi over {} NFTs",
        format_ardi(total),
        token_ids.len()
    );

    let summary = if token_ids.is_empty() {
        format!("Agent {agent_str} owns no NFTs — nothing to claim.")
    } else if total == U256::ZERO {
        format!(
            "Agent {agent_str} owns {} NFT(s) but pending = 0. \
             Either the first daily emission hasn't fired yet, or you've \
             already claimed everything.",
            token_ids.len()
        )
    } else {
        format!(
            "Agent {agent_str} can claim {} $ardi across {} NFT(s). \
             Run `ardi-agent claim` to receive it.",
            format_ardi(total),
            token_ids.len()
        )
    };

    let next_action = if total == U256::ZERO { "review" } else { "review" };
    let next_command = if total == U256::ZERO {
        None
    } else {
        Some("ardi-agent claim".to_string())
    };

    Output::success(
        summary,
        json!({
            "address": agent_str,
            "total_pending_wei": total.to_string(),
            "total_pending_ardi": format_ardi(total),
            "nft_count": token_ids.len(),
            "breakdown": breakdown,
        }),
        Internal {
            next_action: next_action.into(),
            next_command,
            ..Default::default()
        },
    )
    .print();

    Ok(())
}

fn read_addr(v: &Value, key: &str) -> Option<String> {
    v.get(key)
        .or_else(|| v.get("contracts").and_then(|c| c.get(key)))
        .and_then(|x| x.as_str())
        .map(|s| s.to_string())
}

/// Format wei to whole-$ardi string (no decimal precision — UI-friendly).
fn format_ardi(wei: U256) -> String {
    let denom = U256::from(10u64).pow(U256::from(18u64));
    let whole = wei / denom;
    whole.to_string()
}
