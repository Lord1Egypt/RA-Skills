// transfer — move an Ardinal NFT from the agent's wallet to a target
// address (typically the user's MetaMask / main wallet) so they can
// manage it from the browser.
//
// v3 contract guards:
//   * pendingRepairOf[tokenId] != 0 → reverts with TokenLocked
//   * pendingFuseOf[tokenId] != 0   → reverts with TokenLocked
// This skill checks both up-front and refuses with a clear message
// instead of paying gas for a doomed tx.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::ArdiNFT;
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::tx;
use crate::log_info;

pub fn run(server_url: &str, token_id: u64, to_str: String) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;
    let to = Address::from_str(&to_str)
        .map_err(|e| anyhow!("--to is not a valid 0x-address: {e}"))?;
    if to == Address::ZERO {
        return Err(anyhow!("--to cannot be zero address"));
    }
    if to == agent {
        return Err(anyhow!("--to is the agent's own address; nothing to transfer"));
    }

    let api = ApiClient::new(server_url)?;
    let cfg: serde_json::Value = api
        .get_json("/v1/chain/contracts")
        .or_else(|_| api.get_json("/v1/health"))
        .unwrap_or_default();
    let nft_addr_str = read_addr(&cfg, "ardi_nft")
        .or_else(|| std::env::var("ARDI_NFT_ADDR").ok())
        .ok_or_else(|| anyhow!("server didn't return ardi_nft; set ARDI_NFT_ADDR env"))?;
    let nft_addr = Address::from_str(&nft_addr_str)?;

    let token_id_u = U256::from(token_id);

    // Pre-flight: ownership + lock checks.
    let owner_raw = tx::view_call(
        &nft_addr,
        ArdiNFT::ownerOfCall { tokenId: token_id_u }.abi_encode(),
    )?;
    let owner = ArdiNFT::ownerOfCall::abi_decode_returns(&owner_raw, true)?._0;
    if owner != agent {
        Output::error(
            format!(
                "tokenId {token_id} is owned by 0x{:x}, not by us (0x{:x}). \
                 Only the current owner can transfer.",
                owner, agent
            ),
            "NOT_TOKEN_OWNER",
            "validation",
            false,
            "Run `ardi-agent commits` to find a tokenId you own, or transfer was already done.",
            Internal {
                next_action: "rerun_listing".into(),
                next_command: Some("ardi-agent commits".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    let pending_repair_raw = tx::view_call(
        &nft_addr,
        ArdiNFT::pendingRepairOfCall { tokenId: token_id_u }.abi_encode(),
    )?;
    let pending_repair = ArdiNFT::pendingRepairOfCall::abi_decode_returns(&pending_repair_raw, true)?._0;

    let pending_fuse_raw = tx::view_call(
        &nft_addr,
        ArdiNFT::pendingFuseOfCall { tokenId: token_id_u }.abi_encode(),
    )?;
    let pending_fuse = ArdiNFT::pendingFuseOfCall::abi_decode_returns(&pending_fuse_raw, true)?._0;

    if pending_repair != U256::ZERO || pending_fuse != U256::ZERO {
        let kind = if pending_repair != U256::ZERO { "repair" } else { "fuse" };
        Output::error(
            format!(
                "tokenId {token_id} is locked by an in-flight {kind} VRF request. \
                 Wait for the callback to fire (~30s under normal Chainlink load), \
                 or after 6h call `ardi-agent` cleanup commands. Then retry."
            ),
            "TOKEN_LOCKED",
            "state",
            true,
            "Wait ~30s and retry; v3 blocks transfers while VRF is pending so the request can't be re-routed mid-flight.",
            Internal {
                next_action: "wait_vrf".into(),
                next_command: Some(format!("ardi-agent transfer --token-id {token_id} --to {to_str}")),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    log_info!("transfer: tokenId={token_id} from=0x{:x} to=0x{:x}", agent, to);
    let data = tx::calldata_transfer_nft(agent, to, token_id_u);
    let tx_obj = tx::build_tx(&agent, &nft_addr, data, 0, 200_000)?;
    let tx_hash = tx::send_and_wait(&tx_obj).context("send transferFrom tx")?;

    Output::success(
        format!(
            "Transferred Ardinal {token_id} to {to_str}. From this point on the \
             new owner can repair / claim it from the browser without touching \
             the agent's wallet."
        ),
        json!({
            "token_id": token_id,
            "from": format!("0x{:x}", agent),
            "to": to_str,
            "tx_hash": tx_hash,
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
