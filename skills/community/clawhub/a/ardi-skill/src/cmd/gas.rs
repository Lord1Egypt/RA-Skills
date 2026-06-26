// gas — Base ETH balance check + refill guidance.
//
// Cost model (per epoch, worst-case full participation):
//   commit × 5      80k gas each = 400k
//   commit bond × 5 0.001 ETH each = 0.005 ETH (refunded if not winning)
//   reveal × 5      120k gas each = 600k
//   inscribe × 5    150k gas each = 750k
//   total gas       ≈ 1.75M gas
//   @ 1 gwei worst  ≈ 0.00175 ETH per epoch
//
// Recommended initial fund: 0.05 ETH = ~30 epochs of full participation
// or 100s of partial-participation epochs. Refill threshold: 0.01 ETH.

use anyhow::Result;
use alloy_primitives::Address;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::output::{Internal, Output};
use crate::tx;

pub const MIN_ETH: f64 = 0.003; // hard floor — refuse new commits below this
pub const RECOMMENDED_INITIAL_ETH: f64 = 0.05;
pub const REFILL_THRESHOLD_ETH: f64 = 0.01;

#[derive(Debug)]
pub struct GasCheck {
    pub balance_wei: u128,
    pub balance_eth: f64,
    pub min_eth: f64,
    pub recommended_eth: f64,
    pub sufficient: bool,
    pub needs_refill_soon: bool,
}

/// Returns a low-balance warning payload + chat-friendly message line if
/// the wallet balance is below the refill threshold or the hard floor.
/// Other commands call this after successful txs so the LLM surfaces
/// "you should top up soon" before the agent forgets.
pub fn low_balance_warning(address: &str) -> Option<(serde_json::Value, String)> {
    let g = check_balance(address).ok()?;
    if !g.needs_refill_soon && g.sufficient {
        return None;
    }
    let level = if !g.sufficient { "critical" } else { "warning" };
    let msg = if !g.sufficient {
        format!(
            "⚠ CRITICAL: wallet has only {:.6} ETH (below {:.6} floor) — \
             new commits will be refused. Send {:.4} ETH on Base mainnet to {address}.",
            g.balance_eth, g.min_eth, g.recommended_eth
        )
    } else {
        format!(
            "⚠ Low balance: {:.6} ETH left (refill threshold {:.6}) — \
             top up {:.4} ETH on Base mainnet to {address} soon.",
            g.balance_eth, REFILL_THRESHOLD_ETH, g.recommended_eth
        )
    };
    Some((
        serde_json::json!({
            "level": level,
            "balance_eth": g.balance_eth,
            "floor_eth": g.min_eth,
            "refill_threshold_eth": REFILL_THRESHOLD_ETH,
            "recommended_eth": g.recommended_eth,
            "fund_address": address,
            "fund_chain": "Base mainnet (chain id 8453)",
        }),
        msg,
    ))
}

pub fn check_balance(address: &str) -> Result<GasCheck> {
    let addr = Address::from_str(address)
        .map_err(|e| anyhow::anyhow!("invalid address {address}: {e}"))?;
    let bal = tx::eth_balance(&addr)?;
    let eth = (bal as f64) / 1e18;
    Ok(GasCheck {
        balance_wei: bal,
        balance_eth: eth,
        min_eth: MIN_ETH,
        recommended_eth: RECOMMENDED_INITIAL_ETH,
        sufficient: eth >= MIN_ETH,
        needs_refill_soon: eth < REFILL_THRESHOLD_ETH,
    })
}

pub fn run(_server_url: &str) -> Result<()> {
    let address = get_address()?;
    let g = check_balance(&address)?;

    let lines = vec![
        format!("Wallet:        {address}"),
        format!("Base ETH:      {:.6} ETH", g.balance_eth),
        format!("Floor:         {:.6} ETH (commits refused below)", g.min_eth),
        format!("Refill at:     {:.6} ETH", REFILL_THRESHOLD_ETH),
        format!("Recommended:   {:.4} ETH initial fund", g.recommended_eth),
        String::new(),
        format!(
            "Per-epoch worst case: ~0.0017 ETH (full 5 commits + 5 reveals + 5 mints @ 1 gwei)"
        ),
        format!("Per-epoch typical:    ~0.0003 ETH (1-2 commits, occasional mint)"),
        format!("0.05 ETH typically lasts 5-10 days at 6min epochs (gas scales with the 5-commit cap, not riddle count)."),
    ];

    let next = if !g.sufficient {
        Internal {
            next_action: "fund_gas".into(),
            next_command: Some(format!(
                "Send {:.4} ETH on Base mainnet to {address}",
                g.recommended_eth
            )),
            ..Default::default()
        }
    } else if g.needs_refill_soon {
        Internal {
            next_action: "warn_refill_soon".into(),
            next_command: Some(format!(
                "Top up to ~{:.4} ETH soon. Send to {address} on Base mainnet.",
                g.recommended_eth
            )),
            ..Default::default()
        }
    } else {
        Internal {
            next_action: "ok".into(),
            next_command: Some("ardi-agent preflight".into()),
            ..Default::default()
        }
    };

    if g.sufficient {
        Output::success(
            lines.join("\n"),
            json!({
                "address": address,
                "balance_eth": g.balance_eth,
                "balance_wei": g.balance_wei.to_string(),
                "needs_refill_soon": g.needs_refill_soon,
            }),
            next,
        )
        .print();
    } else {
        Output::error(
            lines.join("\n"),
            "INSUFFICIENT_GAS",
            "balance",
            true,
            format!(
                "Send at least {:.4} ETH to {address} on Base mainnet, then re-run `ardi-agent gas`.",
                g.recommended_eth
            ),
            next,
        )
        .print();
    }

    Ok(())
}
