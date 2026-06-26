// claim — pull accumulated $ardi rewards from the EmissionDistributor.
//
// v3.2 (mint-on-claim, reward-follows-NFT):
//   - reward is attributed per tokenId, not per address
//   - claim verifies ownerOf == msg.sender for each tokenId
//   - distributor calls external WorknetManager.batchMint to mint fresh
//     $ardi to the agent (no pre-funding; no transferFrom)
//   - if no token_ids are passed, we auto-fetch every NFT this agent owns
//     from the coordinator and include all of them in one claim tx

use anyhow::{anyhow, Context, Result};
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

pub fn run(server_url: &str, token_ids: Vec<u64>) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;
    let api = ApiClient::new(server_url)?;

    let cfg: Value = api
        .get_json("/v1/chain/contracts")
        .or_else(|_| api.get_json("/v1/health"))
        .unwrap_or_default();
    let dist_addr = read_addr(&cfg, "emission_distributor")
        .or_else(|| std::env::var("EMISSION_DISTRIBUTOR_ADDR").ok())
        .ok_or_else(|| {
            anyhow!(
                "server didn't return emission_distributor; set EMISSION_DISTRIBUTOR_ADDR env"
            )
        })?;
    let dist_addr = Address::from_str(&dist_addr)?;

    // v3.2 default: claim across every NFT the agent owns. Operator can
    // still narrow with --token-id if they want.
    let token_ids: Vec<u64> = if token_ids.is_empty() {
        let state: Option<Value> = api
            .try_get_json(&format!("/v1/agent/{agent_str}/state"))
            .unwrap_or(None);
        let owned: Vec<u64> = state
            .as_ref()
            .and_then(|v| v.get("mints").and_then(|m| m.as_array()))
            .map(|arr| {
                arr.iter()
                    .filter_map(|m| m.get("token_id").and_then(|v| v.as_u64()))
                    .collect()
            })
            .unwrap_or_default();
        log_info!(
            "claim: auto-fetched {} owned NFTs from coord",
            owned.len()
        );
        owned
    } else {
        token_ids
    };

    let token_ids_u: Vec<U256> = token_ids.iter().map(|&t| U256::from(t)).collect();

    // Pre-flight: print pending so the agent knows what they're getting.
    let pending_raw = tx::view_call(
        &dist_addr,
        EmissionDistributor::pendingForCall {
            holder: agent,
            tokenIds: token_ids_u.clone(),
        }
        .abi_encode(),
    )?;
    let pending = EmissionDistributor::pendingForCall::abi_decode_returns(&pending_raw, true)?._0;
    log_info!("claim: pending={pending} ardi over {} tokens", token_ids.len());

    if pending == U256::ZERO {
        Output::success(
            "Nothing to claim - pending balance is zero.".to_string(),
            json!({ "pending_wei": "0" }),
            Internal {
                next_action: "skip".into(),
                next_command: None,
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    let data = tx::calldata_claim(token_ids_u);
    // v3.2 claim: ownerOf check per token + batchMint external call. Gas
    // scales with nft count; budget 200K base + 100K per token.
    let gas_limit: u64 = 200_000 + 100_000 * token_ids.len() as u64;
    let tx_obj = tx::build_tx(&agent, &dist_addr, data, 0, gas_limit)?;
    let claim_hash = tx::send_and_wait(&tx_obj).context("send claim tx")?;

    Output::success(
        format!("Claimed {pending} ardi (tx {claim_hash})."),
        json!({
            "claim_tx": claim_hash,
            "amount_wei": pending.to_string(),
            "tokens": token_ids,
        }),
        Internal {
            next_action: "done".into(),
            next_command: None,
            ..Default::default()
        },
    )
    .print();
    Ok(())
}

fn read_addr(v: &serde_json::Value, key: &str) -> Option<String> {
    v.get(key)
        .or_else(|| v.get("contracts").and_then(|c| c.get(key)))
        .and_then(|x| x.as_str())
        .map(|s| s.to_string())
}
