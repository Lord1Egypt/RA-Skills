// repair — pay $ardi fee + request VRF to refresh an NFT's durability.
//
// v3 mechanic: each NFT decays 1 durability/day; repair restores to full and
// rolls a 1% VRF failure roll. Failure → NFT becomes broken (must fuse to
// revive). Success → NFT keeps earning emission.
//
// Async: repair() returns a requestId; the actual outcome lands later when
// Chainlink VRF callback fires (~30s on Base). The skill does not wait for
// the callback — it returns after the repair tx receipt confirms.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::{ArdiNFT, IERC20};
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::tx;
use crate::log_info;

pub fn run(server_url: &str, token_id: u64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;
    let api = ApiClient::new(server_url)?;

    // Fetch contract addresses from the server (canonical config).
    let cfg: serde_json::Value = api
        .get_json("/v1/chain/contracts")
        .or_else(|_| api.get_json("/v1/health"))
        .unwrap_or_default();
    let nft_addr = read_addr(&cfg, "ardi_nft").or_else(|| std::env::var("ARDI_NFT_ADDR").ok())
        .ok_or_else(|| anyhow!("server didn't return ardi_nft address; set ARDI_NFT_ADDR env"))?;
    let nft_addr = Address::from_str(&nft_addr)?;
    let ardi_addr = read_addr(&cfg, "ardi_token")
        .or_else(|| std::env::var("ARDI_TOKEN_ADDR").ok())
        .ok_or_else(|| anyhow!("server didn't return ardi_token address; set ARDI_TOKEN_ADDR env"))?;
    let ardi_addr = Address::from_str(&ardi_addr)?;

    let token_id_u = U256::from(token_id);

    // 1. Pull repair fee + current allowance.
    let fee_raw = tx::view_call(
        &nft_addr,
        ArdiNFT::repairFeeCall { tokenId: token_id_u }.abi_encode(),
    )?;
    let fee = ArdiNFT::repairFeeCall::abi_decode_returns(&fee_raw, true)?._0;

    let allowance_raw = tx::view_call(
        &ardi_addr,
        IERC20::allowanceCall {
            owner: agent,
            spender: nft_addr,
        }
        .abi_encode(),
    )?;
    let allowance = IERC20::allowanceCall::abi_decode_returns(&allowance_raw, true)?._0;

    log_info!("repair: tokenId={token_id} fee={fee} allowance={allowance}");

    // 2. Approve if short. Approve a generous batch so subsequent repairs
    // don't need a second tx.
    if allowance < fee {
        let approve_amount = fee.saturating_mul(U256::from(20u64));
        let data = tx::calldata_approve(nft_addr, approve_amount);
        let tx_obj = tx::build_tx(&agent, &ardi_addr, data, 0, 80_000)?;
        let approve_hash = tx::send_and_wait(&tx_obj).context("send approve tx")?;
        log_info!("repair: approve tx {approve_hash}");
    }

    // 3. Call repair(tokenId).
    let data = tx::calldata_repair(token_id_u);
    let tx_obj = tx::build_tx(&agent, &nft_addr, data, 0, 350_000)?;
    let repair_hash = tx::send_and_wait(&tx_obj).context("send repair tx")?;
    log_info!("repair: tx submitted {repair_hash}");

    Output::success(
        format!(
            "Repair requested for tokenId {token_id} (fee {fee} ardi). \
             Outcome lands ~30s after Chainlink VRF callback. 1% chance of \
             failure → NFT becomes broken and requires fuse to revive."
        ),
        json!({
            "token_id": token_id,
            "repair_tx": repair_hash,
            "fee_wei": fee.to_string(),
            "expected_callback_seconds": 30,
        }),
        Internal {
            next_action: "wait_vrf".into(),
            next_command: Some(format!("ardi-agent status")),
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
