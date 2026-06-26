// status — combined view: address, AWP registration, ETH balance, stake, recent activity.

use anyhow::Result;
use serde_json::{json, Value};

use crate::auth::get_address;
use crate::awp_register;
use crate::client::ApiClient;
use crate::cmd::commits::BASESCAN;
use crate::output::{Internal, Output};
use crate::{cmd, log_info};

pub fn run(server_url: &str) -> Result<()> {
    let address = get_address()?;
    log_info!("status: address = {address}");

    let registered = awp_register::check_registration(&address).unwrap_or(false);
    let gas = cmd::gas::check_balance(&address)?;

    let api = ApiClient::new(server_url)?;
    let coord_health = api.ping().ok();
    let mut agent_state: Option<Value> = api
        .try_get_json(&format!("/v1/agent/{address}/state"))
        .unwrap_or(None);

    // Enrich each mint with a basescan token link so the LLM can hand the
    // operator a one-click verification URL — pre-v0.5.10 the user had to
    // run `cast call` themselves to confirm "did I really mint that?".
    let nft_addr = std::env::var("ARDI_NFT_ADDR")
        .unwrap_or_else(|_| "0xf68425D0d451699d0d766150634E436Acd2F05A1".to_string());
    if let Some(state) = agent_state.as_mut() {
        if let Some(mints) = state.get_mut("mints").and_then(|v| v.as_array_mut()) {
            for m in mints.iter_mut() {
                let tid = m
                    .get("token_id")
                    .and_then(|v| v.as_u64())
                    .or_else(|| m.get("tokenId").and_then(|v| v.as_u64()));
                if let Some(t) = tid {
                    if let Some(obj) = m.as_object_mut() {
                        obj.insert(
                            "basescan_url".into(),
                            json!(format!("{BASESCAN}/token/{nft_addr}/{t}")),
                        );
                    }
                }
            }
        }
    }

    let address_url = format!("{BASESCAN}/address/{address}");

    let summary = vec![
        format!("Agent address     : {address}"),
        format!("Basescan          : {address_url}"),
        format!(
            "AWP registered    : {}",
            if registered { "yes" } else { "no" }
        ),
        format!("Base ETH balance  : {:.6} ETH", gas.balance_eth),
        format!(
            "Coordinator       : {}",
            if coord_health.is_some() { "reachable" } else { "UNREACHABLE" }
        ),
        format!(
            "Stake state       : {}",
            agent_state
                .as_ref()
                .map(|v| v.to_string())
                .unwrap_or_else(|| "(no state)".into())
        ),
    ];

    Output::success(
        summary.join("\n"),
        json!({
            "address": address,
            "address_url": address_url,
            "registered": registered,
            "balance_eth": gas.balance_eth,
            "coord_reachable": coord_health.is_some(),
            "agent_state": agent_state,
        }),
        Internal {
            next_action: "review".into(),
            next_command: Some("ardi-agent preflight".into()),
            ..Default::default()
        },
    )
    .print();

    Ok(())
}
