// schema — strong-typed mirrors of every wire shape this skill consumes.
//
// WHY: we accumulated ~5 incidents (v0.3.1, v0.3.3, v0.3.4, v0.4.1,
// v0.5.3) where coord-rs / awp-wallet / awp-rootnet quietly changed
// a field's case or type and the skill silently fell through to
// .unwrap_or(default). Each incident took 30+ minutes to diagnose
// from a "preflight passes but commit reverts" symptom.
//
// HOW: every external response gets a #[derive(Deserialize)] struct
// here. Call sites use `serde_json::from_value::<T>(json)?` which:
//   - Errors loudly at the SHAPE BOUNDARY ("missing field epochId" /
//     "invalid type: number, expected string") instead of fumbling on.
//   - Documents the contract — you can read this file and see exactly
//     what the skill expects from each upstream.
//   - Survives field renames via #[serde(rename = "x", alias = "y")]
//     without manual .or_else() chains.
//
// IMPORTANT: keep these types MINIMAL — only fields the skill reads.
// Adding fields the skill doesn't use creates rot and forces
// deserialize failures when servers add unrelated optional fields.
// Use #[serde(deny_unknown_fields)] only on payloads we control end
// to end (none here).

use serde::{Deserialize, Deserializer};
use serde_json::Value;

// ============================================================================
// coord-rs HTTP API — JSON over POST/GET to the coordinator
// ============================================================================

/// `GET /v1/epoch/current` — current commit-able epoch with riddles.
/// coord-rs serializes camelCase via #[serde(rename = "...")] on
/// `CurrentEpoch` in coord-rs/crates/ardi-core/src/types.rs.
#[derive(Debug, Clone, Deserialize)]
pub struct CurrentEpoch {
    #[serde(rename = "epochId", alias = "epoch_id")]
    pub epoch_id: u64,
    #[serde(rename = "startTs", alias = "start_ts", default)]
    pub start_ts: i64,
    #[serde(rename = "commitDeadline", alias = "commit_deadline")]
    pub commit_deadline: i64,
    #[serde(rename = "revealDeadline", alias = "reveal_deadline")]
    pub reveal_deadline: i64,
    #[serde(rename = "chainId", alias = "chain_id", default)]
    pub chain_id: u64,
    /// EpochDraw contract address — required by `commit` to know where
    /// to send the tx. Failure to deserialize here is the reason every
    /// commit attempt failed in the v0.5.3 incident.
    #[serde(rename = "epochDrawContract", alias = "epoch_draw_contract")]
    pub epoch_draw_contract: String,
    #[serde(rename = "ardiNftContract", alias = "ardi_nft_contract", default)]
    pub ardi_nft_contract: String,
    pub riddles: Vec<Riddle>,
}

/// One riddle inside a `CurrentEpoch`.
#[derive(Debug, Clone, Deserialize)]
pub struct Riddle {
    #[serde(rename = "wordId", alias = "word_id")]
    pub word_id: u64,
    pub riddle: String,
    #[serde(default)]
    pub power: u16,
    #[serde(default)]
    pub rarity: String,
    #[serde(default)]
    pub language: String,
    #[serde(rename = "languageId", alias = "language_id", default)]
    pub language_id: u8,
    #[serde(rename = "hintLevel", alias = "hint_level", default)]
    pub hint_level: u8,
    /// v3.1 fields — empty string for legacy mock payloads.
    #[serde(default)]
    pub theme: String,
    #[serde(default)]
    pub element: String,
}

/// `GET /v1/agent/{addr}/state` — agent's mint history + remaining cap.
/// Used by preflight + status. NOTE: this endpoint does NOT return an
/// `eligible` field (that lives on chain — see stake::check_eligible_onchain).
#[derive(Debug, Clone, Deserialize)]
pub struct AgentState {
    pub agent: String,
    #[serde(default)]
    pub mints: Vec<MintRow>,
    #[serde(rename = "mintCount", alias = "mint_count", default)]
    pub mint_count: u32,
    #[serde(rename = "remainingMintCap", alias = "remaining_mint_cap", default)]
    pub remaining_mint_cap: u32,
}

#[derive(Debug, Clone, Deserialize)]
pub struct MintRow {
    #[serde(rename = "wordId", alias = "word_id")]
    pub word_id: u64,
    #[serde(rename = "tokenId", alias = "token_id")]
    pub token_id: u64,
    #[serde(rename = "epochId", alias = "epoch_id", default)]
    pub epoch_id: Option<u64>,
    #[serde(rename = "mintedAt", alias = "minted_at", default)]
    pub minted_at: i64,
}

// ============================================================================
// AWP rootnet RPC — JSON-RPC 2.0 to api.awp.sh/v2
// ============================================================================

/// `registry.get` result. Returns ALL on-chain contract addresses for the
/// chain. Triggered v0.3.3 when a previous version expected `result` to be
/// the bare address string.
#[derive(Debug, Clone, Deserialize)]
pub struct RegistryGetResult {
    #[serde(rename = "chainId")]
    pub chain_id: u64,
    #[serde(rename = "awpRegistry")]
    pub awp_registry: String,
    #[serde(rename = "awpToken", default)]
    pub awp_token: Option<String>,
    #[serde(rename = "awpAllocator", default)]
    pub awp_allocator: Option<String>,
    #[serde(rename = "awpEmission", default)]
    pub awp_emission: Option<String>,
}

/// `nonce.get` result. Returns `{ nonce: N }`, NOT a bare integer.
/// Triggered v0.3.3.
#[derive(Debug, Clone, Deserialize)]
pub struct NonceGetResult {
    pub nonce: u64,
}

/// `address.check` result.
#[derive(Debug, Clone, Deserialize)]
pub struct AddressCheckResult {
    #[serde(rename = "isRegistered")]
    pub is_registered: bool,
    #[serde(default)]
    pub recipient: Option<String>,
}

/// `staking.getAllocationsByAgentSubnet` row. amount is JSON Number on
/// the wire (NOT string) — triggered v0.3.1 silent failure. Custom
/// deserializer accepts both forms.
#[derive(Debug, Clone, Deserialize)]
pub struct AllocationRow {
    pub chain_id: i64,
    pub user_address: String,
    #[serde(deserialize_with = "deser_amount_any")]
    pub amount: String,
    pub frozen: bool,
}

fn deser_amount_any<'de, D: Deserializer<'de>>(d: D) -> std::result::Result<String, D::Error> {
    // Mirrors awp_rpc::deser_amount_any. Number / String both accepted.
    // Number relies on serde_json's `arbitrary_precision` feature so
    // 1e22-scale values don't lose precision via f64.
    let v = Value::deserialize(d)?;
    match v {
        Value::String(s) => Ok(s),
        Value::Number(n) => Ok(n.to_string()),
        other => Err(serde::de::Error::custom(format!(
            "amount: expected string or number, got {other:?}"
        ))),
    }
}

// ============================================================================
// awp-wallet CLI — stdout JSON from `awp-wallet <subcmd>`
// ============================================================================

/// `awp-wallet sign-typed-data --data <json>` → signature + signer.
#[derive(Debug, Clone, Deserialize)]
pub struct WalletSignTypedDataResult {
    pub signature: String,
    #[serde(default)]
    pub signer: Option<String>,
}

/// `awp-wallet send-tx --to ... --data ...` → broadcast tx hash.
#[derive(Debug, Clone, Deserialize)]
pub struct WalletSendTxResult {
    #[serde(default)]
    pub status: Option<String>,
    /// Newer awp-wallet returns `txHash`; older builds may use
    /// `transactionHash` or `hash`. All three are accepted.
    #[serde(rename = "txHash", alias = "transactionHash", alias = "hash")]
    pub tx_hash: String,
    #[serde(default)]
    pub from: Option<String>,
    #[serde(default)]
    pub to: Option<String>,
}

/// `awp-wallet receive` → wallet's EOA address.
#[derive(Debug, Clone, Deserialize)]
pub struct WalletReceiveResult {
    /// awp-wallet >= 1.4 returns `eoaAddress`; older `address`.
    #[serde(rename = "eoaAddress", alias = "address")]
    pub address: String,
}

// ============================================================================
// Helpers
// ============================================================================

/// Convenience: try to parse a serde_json::Value as T, with a helpful
/// context string on failure ("decode <name>: <serde error>: <raw json>").
pub fn parse<T>(name: &str, v: Value) -> anyhow::Result<T>
where
    T: serde::de::DeserializeOwned,
{
    serde_json::from_value::<T>(v.clone()).map_err(|e| {
        anyhow::anyhow!(
            "decode {name}: {e}\n  raw: {}",
            serde_json::to_string(&v).unwrap_or_else(|_| "<unserializable>".into())
        )
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn current_epoch_decodes_camel() {
        let raw = r#"{
            "epochId": 12,
            "commitDeadline": 1777750000,
            "revealDeadline": 1777750180,
            "epochDrawContract": "0x21c2eba56c440c292a32f0fdd16c26be13d391bb",
            "ardiNftContract": "0x91734696e8164cbf79b666569d2504b0e21218f6",
            "chainId": 8453,
            "startTs": 1777749820,
            "riddles": []
        }"#;
        let e: CurrentEpoch = serde_json::from_str(raw).unwrap();
        assert_eq!(e.epoch_id, 12);
        assert_eq!(e.commit_deadline, 1777750000);
        assert!(e.epoch_draw_contract.starts_with("0x21c2"));
    }

    #[test]
    fn current_epoch_decodes_snake_legacy() {
        // Legacy mock / older coord-rs builds with snake_case.
        let raw = r#"{
            "epoch_id": 5,
            "commit_deadline": 1,
            "reveal_deadline": 2,
            "epoch_draw_contract": "0xabc",
            "riddles": []
        }"#;
        let e: CurrentEpoch = serde_json::from_str(raw).unwrap();
        assert_eq!(e.epoch_id, 5);
    }

    #[test]
    fn allocation_row_decodes_number_amount() {
        let raw = r#"{
            "chain_id": 8453,
            "user_address": "0x800d05fd8e251c288e22809b79d31f22ab088555",
            "amount": 10000000000000000000000,
            "frozen": false
        }"#;
        let a: AllocationRow = serde_json::from_str(raw).unwrap();
        assert_eq!(a.amount, "10000000000000000000000");
    }

    #[test]
    fn nonce_get_result() {
        let raw = r#"{"nonce": 42}"#;
        let n: NonceGetResult = serde_json::from_str(raw).unwrap();
        assert_eq!(n.nonce, 42);
    }

    #[test]
    fn registry_get_result() {
        let raw = r#"{
            "chainId": 8453,
            "awpRegistry": "0xR",
            "awpToken": "0xT"
        }"#;
        let r: RegistryGetResult = serde_json::from_str(raw).unwrap();
        assert_eq!(r.awp_registry, "0xR");
        assert_eq!(r.awp_token.as_deref(), Some("0xT"));
        assert!(r.awp_emission.is_none());
    }

    #[test]
    fn missing_required_field_errors_loudly() {
        // Missing epochDrawContract should fail with a clear message.
        let raw = r#"{
            "epochId": 12,
            "commitDeadline": 1, "revealDeadline": 2,
            "riddles": []
        }"#;
        let err = serde_json::from_str::<CurrentEpoch>(raw).unwrap_err();
        let msg = format!("{err}");
        assert!(
            msg.contains("epochDrawContract") || msg.contains("missing field"),
            "expected missing-field error, got: {msg}"
        );
    }
}
