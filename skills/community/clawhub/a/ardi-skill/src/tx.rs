// Transaction helpers — calldata builders + send_tx via awp-wallet bridge
// + receipt polling against Base RPC.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, B256, U256};
use alloy_sol_types::SolCall;
use serde_json::{json, Value};
use std::time::Duration;

use crate::chain::{ArdiEpochDraw, ArdiNFT, ArdiOTC, EmissionDistributor, IERC20, IERC721};
use crate::rpc;
use crate::wallet;

pub const BASE_CHAIN_ID: u64 = 8453;
pub const COMMIT_BOND_WEI: u128 = 10_000_000_000_000; // 0.00001 ETH (matches contract)

pub fn nonce_for(addr: &Address) -> Result<u64> {
    let r = rpc::call(
        "eth_getTransactionCount",
        json!([format!("0x{:x}", addr), "pending"]),
    )?;
    let s = r.as_str().unwrap_or("0x0").trim_start_matches("0x");
    Ok(u64::from_str_radix(s, 16).unwrap_or(0))
}

pub fn gas_price_gwei() -> Result<u128> {
    let r = rpc::call("eth_gasPrice", json!([]))?;
    let s = r.as_str().unwrap_or("0x0").trim_start_matches("0x");
    Ok(u128::from_str_radix(s, 16).unwrap_or(0))
}

/// Fetch raw eth balance in wei.
pub fn eth_balance(addr: &Address) -> Result<u128> {
    let r = rpc::call(
        "eth_getBalance",
        json!([format!("0x{:x}", addr), "latest"]),
    )?;
    let s = r.as_str().unwrap_or("0x0").trim_start_matches("0x");
    Ok(u128::from_str_radix(s, 16).unwrap_or(0))
}

/// Build a unsigned EIP-1559 tx envelope for awp-wallet to sign + broadcast.
pub fn build_tx(
    from: &Address,
    to: &Address,
    data: Vec<u8>,
    value_wei: u128,
    gas_limit: u64,
) -> Result<Value> {
    let nonce = nonce_for(from)?;
    let base_fee = gas_price_gwei()?;
    // Base mainnet is super cheap; pay 2× current as priority+max for headroom.
    let max_fee = (base_fee * 2).max(1_000_000); // 0.001 gwei floor
    let max_priority = 1_000_000u128; // 0.001 gwei

    Ok(json!({
        "chainId": BASE_CHAIN_ID,
        "from": format!("0x{:x}", from),
        "to": format!("0x{:x}", to),
        "data": format!("0x{}", hex::encode(&data)),
        "value": format!("0x{:x}", value_wei),
        "nonce": nonce,
        "gas": format!("0x{:x}", gas_limit),
        "maxFeePerGas": format!("0x{:x}", max_fee),
        "maxPriorityFeePerGas": format!("0x{:x}", max_priority),
        "type": "0x2",
    }))
}

/// Build commit calldata. v3.1: takes a staker LIST. Empty → self-stake fallback.
/// MUST be strict-ascending (= dedup). Skill sorts before calling.
pub fn calldata_commit(epoch_id: u64, word_id: u64, hash: B256, stakers: Vec<Address>) -> Vec<u8> {
    let call = ArdiEpochDraw::commitCall {
        epochId: U256::from(epoch_id),
        wordId: U256::from(word_id),
        hash,
        stakers,
    };
    call.abi_encode()
}

/// v3 reveal — only (guess, nonce). vaultProof is server-side at publishAnswers.
pub fn calldata_reveal(epoch_id: u64, word_id: u64, guess: String, nonce: B256) -> Vec<u8> {
    let call = ArdiEpochDraw::revealCall {
        epochId: U256::from(epoch_id),
        wordId: U256::from(word_id),
        guess,
        nonce,
    };
    call.abi_encode()
}

/// v3 inscribe — power/lang/durability/element come from EpochDraw.getAnswer
/// on chain; only the plaintext word is supplied (verified vs wordHash).
pub fn calldata_inscribe(epoch_id: u64, word_id: u64, word: String) -> Vec<u8> {
    let call = ArdiNFT::inscribeCall {
        epochId: epoch_id,
        wordId: U256::from(word_id),
        word,
    };
    call.abi_encode()
}

pub fn calldata_repair(token_id: U256) -> Vec<u8> {
    ArdiNFT::repairCall { tokenId: token_id }.abi_encode()
}

pub fn calldata_claim(token_ids: Vec<U256>) -> Vec<u8> {
    EmissionDistributor::claimCall { tokenIds: token_ids }.abi_encode()
}

pub fn calldata_approve(spender: Address, amount: U256) -> Vec<u8> {
    IERC20::approveCall { spender, amount }.abi_encode()
}

pub fn calldata_transfer_nft(from: Address, to: Address, token_id: U256) -> Vec<u8> {
    ArdiNFT::transferFromCall { from, to, tokenId: token_id }.abi_encode()
}

pub fn calldata_otc_list(token_id: U256, price_wei: U256) -> Vec<u8> {
    ArdiOTC::listCall { tokenId: token_id, priceWei: price_wei }.abi_encode()
}

pub fn calldata_otc_unlist(token_id: U256) -> Vec<u8> {
    ArdiOTC::unlistCall { tokenId: token_id }.abi_encode()
}

pub fn calldata_otc_buy(token_id: U256) -> Vec<u8> {
    ArdiOTC::buyCall { tokenId: token_id }.abi_encode()
}

pub fn calldata_set_approval_for_all(operator: Address, approved: bool) -> Vec<u8> {
    IERC721::setApprovalForAllCall { operator, approved }.abi_encode()
}

/// Wait for a tx receipt up to `timeout_secs`, return success bool + block.
pub fn wait_receipt(tx_hash: &str, timeout_secs: u64) -> Result<(bool, u64)> {
    let deadline = std::time::Instant::now() + Duration::from_secs(timeout_secs);
    loop {
        let r = rpc::call("eth_getTransactionReceipt", json!([tx_hash]))?;
        if !r.is_null() {
            let status = r
                .get("status")
                .and_then(|v| v.as_str())
                .unwrap_or("0x0");
            let success = status == "0x1";
            let block = r
                .get("blockNumber")
                .and_then(|v| v.as_str())
                .map(|s| u64::from_str_radix(s.trim_start_matches("0x"), 16).unwrap_or(0))
                .unwrap_or(0);
            return Ok((success, block));
        }
        if std::time::Instant::now() >= deadline {
            return Err(anyhow!("receipt timeout for {tx_hash}"));
        }
        std::thread::sleep(Duration::from_secs(2));
    }
}

/// Send + actually wait for the receipt and confirm `status == 0x1`.
///
/// Pre-v0.5.6 this was a lie — it just returned the broadcast hash,
/// never polled the receipt. Effect: a tx that reverted on chain
/// (e.g. CommitWindowClosed) returned "Ok" to commit.rs, which then
/// persisted local state as if the commit landed. User saw
/// "✓ committed" + tx hash, but on-chain commits[] was empty.
///
/// Now: poll eth_getTransactionReceipt up to RECEIPT_TIMEOUT_SEC.
/// If status != 0x1, return Err with the revert info — caller's `?`
/// propagates the failure and DOESN'T persist the optimistic state.
pub fn send_and_wait(tx: &Value) -> Result<String> {
    const RECEIPT_TIMEOUT_SEC: u64 = 90;
    let hash = wallet::send_tx(tx)?;
    let (success, block) = wait_receipt(&hash, RECEIPT_TIMEOUT_SEC)
        .with_context(|| format!("wait_receipt({hash})"))?;
    if !success {
        return Err(anyhow!(
            "tx {hash} REVERTED on chain (block {block}). \
             Skill state NOT persisted. Common causes: CommitWindowClosed, \
             InsufficientStake, AlreadyCommitted, EpochUnknown. Decode revert \
             selector with: cast call <to> <input> --from <agent> --rpc-url \
             https://mainnet.base.org"
        ));
    }
    Ok(hash)
}

/// View call helper — eth_call returning hex string result.
pub fn view_call(to: &Address, data: Vec<u8>) -> Result<Vec<u8>> {
    let r = rpc::call(
        "eth_call",
        json!([
            { "to": format!("0x{:x}", to), "data": format!("0x{}", hex::encode(data)) },
            "latest"
        ]),
    )?;
    let s = r.as_str().unwrap_or("0x").trim_start_matches("0x");
    Ok(hex::decode(s).unwrap_or_default())
}
