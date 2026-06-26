// AWP network registration — gasless EIP-712 register via the AWP relay.
// Mirrors prediction-skill's awp_register.rs, adapted for chainId=8453 only
// (Ardi is mainnet from launch).

use anyhow::{anyhow, Context, Result};
use reqwest::blocking::Client;
use serde_json::{json, Value};
use std::time::Duration;

use crate::wallet;
use crate::{log_debug, log_info};

const AWP_API_BASE: &str = "https://api.awp.sh/v2";
const AWP_RELAY_BASE: &str = "https://api.awp.sh/api";
const CHAIN_ID: u64 = 8453;

#[derive(Debug)]
pub struct RegistrationResult {
    pub registered: bool,
    pub auto_registered: bool,
    pub message: String,
}

pub fn check_registration(address: &str) -> Result<bool> {
    let client = build_client();
    let resp = awp_jsonrpc(
        &client,
        "address.check",
        json!({ "address": address, "chainId": CHAIN_ID }),
    )?;
    Ok(is_registered(&resp))
}

pub fn ensure_registered(address: &str) -> Result<RegistrationResult> {
    if check_registration(address)? {
        return Ok(RegistrationResult {
            registered: true,
            auto_registered: false,
            message: "Already registered on AWP network.".into(),
        });
    }

    log_info!("awp_register: not yet registered — preparing gasless EIP-712 SetRecipient...");
    let client = build_client();

    // Get registry contract address + nonce.
    //
    // v2 API note: `registry.get` returns a *structured object*
    // ({chainId, awpRegistry, awpToken, awpAllocator, ...}), NOT a bare
    // address string. Same for `nonce.get` which returns ({nonce: N}),
    // not a bare integer. Earlier versions of this code assumed the
    // primitive form and silently failed at preflight when the API was
    // upgraded — surfaced in the field by external testers (kaito).
    let registry_resp: Value = awp_jsonrpc(&client, "registry.get", json!({ "chainId": CHAIN_ID }))?;
    let registry_result = registry_resp.get("result").cloned()
        .ok_or_else(|| anyhow!("registry.get: missing top-level `result`; got {registry_resp}"))?;
    let registry: crate::schema::RegistryGetResult =
        crate::schema::parse("registry.get", registry_result)?;
    let registry_addr = &registry.awp_registry;

    let nonce_resp: Value = awp_jsonrpc(
        &client,
        "nonce.get",
        json!({ "address": address, "chainId": CHAIN_ID }),
    )?;
    let nonce_result = nonce_resp.get("result").cloned()
        .ok_or_else(|| anyhow!("nonce.get: missing top-level `result`; got {nonce_resp}"))?;
    let nonce_typed: crate::schema::NonceGetResult =
        crate::schema::parse("nonce.get", nonce_result)?;
    let nonce = nonce_typed.nonce;

    let deadline = chrono::Utc::now().timestamp() as u64 + 600;

    // v2 contract uses `user` (not `agent`) in the EIP-712 SetRecipient
    // schema. v0.3.4 only renamed the relay POST field — the typed-data
    // schema kept `agent`, which made the hash diverge from what the
    // contract verifier computes → setRecipientFor() reverts InvalidSignature
    // (selector 0x8baa579f). Production tx confirmed:
    // 0x5b9287c567cae98d0f4a2833bae9d3467f3e116629f1996962b4d3749b6f5023.
    let typed = json!({
        "domain": {
            "name": "AWPRegistry",
            "version": "1",
            "chainId": CHAIN_ID,
            "verifyingContract": registry_addr,
        },
        "types": {
            "SetRecipient": [
                { "name": "user", "type": "address" },
                { "name": "recipient", "type": "address" },
                { "name": "nonce", "type": "uint256" },
                { "name": "deadline", "type": "uint256" },
            ],
        },
        "primaryType": "SetRecipient",
        "message": {
            "user": address,
            "recipient": address,
            "nonce": nonce.to_string(),
            "deadline": deadline.to_string(),
        },
    });

    log_debug!("awp_register: signing typed data: {}", typed);
    let signature = wallet::sign_typed_data(&typed)
        .context("awp-wallet sign-typed-data failed")?;

    let relay_resp: Value = client
        .post(format!("{AWP_RELAY_BASE}/relay/set-recipient"))
        .json(&json!({
            // v2 API: the relay expects "user" (the staker / owner address),
            // not "agent" (which was the v1 name). Confirmed by probing the
            // endpoint: with "agent" it returns 400 "invalid user address";
            // with "user" it advances to signature validation.
            "chainId": CHAIN_ID,
            "user": address,
            "recipient": address,
            "deadline": deadline,
            "signature": signature,
        }))
        .send()
        .context("awp relay POST failed")?
        .json()
        .context("awp relay returned non-JSON")?;
    log_debug!("awp_register: relay response = {}", relay_resp);

    // Poll until registered (or give up after a few tries).
    for _ in 0..5 {
        std::thread::sleep(Duration::from_secs(2));
        if check_registration(address)? {
            return Ok(RegistrationResult {
                registered: true,
                auto_registered: true,
                message: "Auto-registered on AWP network (gasless).".into(),
            });
        }
    }
    Ok(RegistrationResult {
        registered: false,
        auto_registered: false,
        message: format!(
            "Registration submitted but not confirmed yet. Re-run preflight in 30s. Relay response: {relay_resp}"
        ),
    })
}

fn build_client() -> Client {
    Client::builder()
        .timeout(Duration::from_secs(15))
        .user_agent(concat!("ardi-agent/", env!("CARGO_PKG_VERSION")))
        .build()
        .expect("reqwest client")
}

fn awp_jsonrpc(client: &Client, method: &str, params: Value) -> Result<Value> {
    let req = json!({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    });
    let resp: Value = client
        .post(AWP_API_BASE)
        .json(&req)
        .send()
        .with_context(|| format!("AWP JSON-RPC POST {method}"))?
        .json()
        .with_context(|| format!("AWP JSON-RPC parse {method}"))?;
    if let Some(err) = resp.get("error") {
        return Err(anyhow!("AWP JSON-RPC {method} error: {err}"));
    }
    Ok(resp)
}

fn is_registered(resp: &Value) -> bool {
    resp.get("result")
        .and_then(|r| r.get("isRegistered"))
        .and_then(|v| v.as_bool())
        .unwrap_or(false)
}
