// stake — show on-chain stake status across both Ardi + KYA worknets.
//
// v3: queries AWPAllocator directly (was AWPRegistry in v0.1.x). The registry's
// getAgentInfo only surfaces stake when the agent has called bind(staker),
// which KYA-delegated agents never do. AWPAllocator.getAgentStake takes the
// staker explicitly, so we ask the server's indexer (`/v1/agent/{addr}/stakers`)
// for all known stakers backing this agent and check each one. Self-stake
// is checked too as a degenerate case (staker == agent).

use anyhow::Result;
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::collections::BTreeMap;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::{ArdiEpochDraw, AWPAllocator};
use crate::output::{Internal, Output};
use crate::tx;

// Worknet IDs verified 2026-05-02 against AWP API subnets.get:
//   845300000014 = "AWP ARDI Worknet" (aARDI) — self-stakers lock veAWP here
//   845300000012 = "AWP KYA Worknet" (aKYA) — KYA-delegated stakes always go here
// (Earlier versions had these reversed; the contract was hot-fixed via
//  setWorknetIds. Both worknets are still checked OR-style for eligibility.)
const ARDI_WORKNET_ID: &str = "845300000014";
const KYA_WORKNET_ID: &str = "845300000012";
const VE_AWP: &str = "0x0000b534C63D78212f1BDCc315165852793A00A8";
const AWP_ALLOCATOR: &str = "0x0000D6BB5e040E35081b3AaF59DD71b21C9800AA";
// ArdiEpochDraw v3 proxy on Base mainnet — UUPS upgradable, owner-settable
// minStake. We read the threshold LIVE from this proxy so the skill always
// reflects the current contract state instead of a stale constant.
const EPOCH_DRAW: &str = "0xA57d8E6646E063FFd6eae579d4f327b689dA5DC3";
// Display fallback only — used in error messages and JSON when the on-chain
// read fails (e.g. RPC down). Mirrors the value at deploy time but the
// authoritative source is the chain read below.
const MIN_STAKE_AWP_DEFAULT: u128 = 10_000;
const ONE_AWP_WEI: u128 = 1_000_000_000_000_000_000;

/// Lightweight on-chain eligibility probe. Returns true when the agent
/// has summed stake (across both worknets, all known stakers) >= minStake.
/// Used by `preflight` so it doesn't go through the coord-rs cache.
///
/// Two-tier strategy:
/// 1. **Fast path**: AWP rootnet `staking.getAgentWorknetStake` for each
///    worknet — server-side aggregator, returns the exact total in one
///    HTTP call. Covers self-stake AND every delegator across all chains
///    without us needing to enumerate stakers. This is the path that
///    catches the case kaito hit on 2026-05-03 where his agent had
///    delegated stake on Ardi worknet that the indexer-discover path
///    silently missed.
/// 2. **Fallback**: original discover (AWP RPC `getAllocationsByAgentSubnet`)
///    + per-staker on-chain `getAgentStake` probe. Used when the rootnet
///    RPC is unreachable (network partition, server maintenance) — the
///    chain is always the ground truth.
pub fn check_eligible_onchain(agent_str: &str) -> Result<bool> {
    let agent = Address::from_str(agent_str)?;
    let min_stake_wei = read_min_stake_wei().unwrap_or(U256::from(MIN_STAKE_AWP_DEFAULT) * U256::from(ONE_AWP_WEI));

    // ── Fast path — single aggregator call per worknet ─────────────
    if let Ok(rpc) = crate::awp_rpc::AwpRpc::new() {
        let mut total = U256::ZERO;
        let mut fast_path_ok = true;
        for wn in [ARDI_WORKNET_ID, KYA_WORKNET_ID] {
            match rpc.agent_worknet_stake(agent_str, wn) {
                Ok(amount_str) => {
                    if let Ok(v) = U256::from_str_radix(&amount_str, 10) {
                        total = total.saturating_add(v);
                    }
                }
                Err(_) => { fast_path_ok = false; break; }
            }
        }
        if fast_path_ok {
            return Ok(total >= min_stake_wei);
        }
        // else: fall through to the slower discover+probe loop below
    }

    // ── Fallback — discover stakers, probe each (staker, worknet) ──
    let mut stakers: BTreeMap<String, Address> = BTreeMap::new();
    stakers.insert(format!("0x{:x}", agent), agent);
    if let Ok(rpc) = crate::awp_rpc::AwpRpc::new() {
        for wn in [ARDI_WORKNET_ID, KYA_WORKNET_ID] {
            if let Ok(rows) = rpc.allocations_by_agent_worknet(agent_str, wn, None) {
                for r in rows {
                    if let Ok(addr) = Address::from_str(&r.user_address) {
                        stakers.insert(format!("0x{:x}", addr), addr);
                    }
                }
            }
        }
    }
    for (_, &staker) in &stakers {
        for wn in [ARDI_WORKNET_ID, KYA_WORKNET_ID] {
            if let Ok(stake_wei) = read_alloc(staker, agent, wn) {
                if stake_wei >= min_stake_wei {
                    return Ok(true);
                }
            }
        }
    }
    Ok(false)
}

/// Read the live minStake threshold from the EpochDraw contract on Base
/// mainnet. Owner-settable, so we MUST query the chain — never assume.
fn read_min_stake_wei() -> Result<U256> {
    let addr_str = std::env::var("ARDI_EPOCH_DRAW_ADDR").unwrap_or_else(|_| EPOCH_DRAW.to_string());
    let addr = Address::from_str(&addr_str)?;
    let call = ArdiEpochDraw::minStakeCall {};
    let raw = tx::view_call(&addr, call.abi_encode())?;
    let decoded = ArdiEpochDraw::minStakeCall::abi_decode_returns(&raw, true)?;
    Ok(decoded._0)
}

#[derive(Debug, Clone)]
struct CheckedAlloc {
    staker: Address,
    worknet: String,
    stake_wei: U256,
    stake_awp: f64,
    passes: bool,
}

fn read_alloc(staker: Address, agent: Address, worknet_id_str: &str) -> Result<U256> {
    let allocator = Address::from_str(AWP_ALLOCATOR)?;
    let wn = U256::from_str_radix(worknet_id_str, 10)?;
    let call = AWPAllocator::getAgentStakeCall {
        staker,
        agent,
        worknetId: wn,
    };
    let raw = tx::view_call(&allocator, call.abi_encode())?;
    let decoded = AWPAllocator::getAgentStakeCall::abi_decode_returns(&raw, true)?;
    Ok(decoded._0)
}

pub fn run(_server_url: &str) -> Result<()> {
    let address_str = get_address()?;
    let agent = Address::from_str(&address_str)?;
    // v3.1 — read minStake LIVE from EpochDraw. Owner can change it via
    // setMinStake; hardcoding here would silently lie to the user.
    let (min_stake_wei, min_stake_source) = match read_min_stake_wei() {
        Ok(v) => (v, "chain"),
        Err(e) => {
            crate::log_warn!("could not read minStake from chain ({e}); using default {MIN_STAKE_AWP_DEFAULT} AWP");
            (
                U256::from(MIN_STAKE_AWP_DEFAULT) * U256::from(ONE_AWP_WEI),
                "fallback-constant",
            )
        }
    };
    let min_stake_awp = (min_stake_wei.to::<u128>() as f64) / (ONE_AWP_WEI as f64);

    // Build the candidate staker set from AWP rootnet RPC. AWP indexes
    // Allocated events across all chains; we ask both worknets and union
    // the staker addresses, then verify each on chain. Self (agent) is
    // always included so a fresh self-stake doesn't get skipped while AWP
    // is indexing.
    let mut stakers: BTreeMap<String, Address> = BTreeMap::new();
    stakers.insert(format!("0x{:x}", agent), agent);

    let rpc = crate::awp_rpc::AwpRpc::new()?;
    for wn in [ARDI_WORKNET_ID, KYA_WORKNET_ID] {
        if let Ok(rows) = rpc.allocations_by_agent_worknet(&address_str, wn, None) {
            for r in rows {
                if let Ok(addr) = Address::from_str(&r.user_address) {
                    stakers.insert(format!("0x{:x}", addr), addr);
                }
            }
        }
    }

    // Probe each (staker, worknet) pair.
    let mut allocs = Vec::new();
    for (_, &staker) in &stakers {
        for wn in [ARDI_WORKNET_ID, KYA_WORKNET_ID] {
            let stake_wei = read_alloc(staker, agent, wn).unwrap_or(U256::ZERO);
            if stake_wei == U256::ZERO {
                continue;
            }
            let stake_awp = (stake_wei.to::<u128>() as f64) / (ONE_AWP_WEI as f64);
            allocs.push(CheckedAlloc {
                staker,
                worknet: wn.to_string(),
                stake_wei,
                stake_awp,
                passes: stake_wei >= min_stake_wei,
            });
        }
    }

    let passing: Vec<&CheckedAlloc> = allocs.iter().filter(|a| a.passes).collect();
    let eligible = !passing.is_empty();

    let mut lines = vec![
        format!("Agent:                  {address_str}"),
        format!("Threshold (each path):  {} AWP (source: {})", min_stake_awp, min_stake_source),
    ];
    if allocs.is_empty() {
        lines.push("No allocations found across known stakers.".into());
    } else {
        for a in &allocs {
            let wn_label = if a.worknet == ARDI_WORKNET_ID {
                "Ardi"
            } else {
                "KYA "
            };
            lines.push(format!(
                "{wn_label} ({})  staker=0x{:x}  stake={:.2} AWP  →  {}",
                a.worknet,
                a.staker,
                a.stake_awp,
                if a.passes { "PASSES" } else { "below threshold" }
            ));
        }
    }
    lines.push(format!(
        "Status:                 {}",
        if eligible {
            "ELIGIBLE"
        } else {
            "NOT ELIGIBLE"
        }
    ));

    if eligible {
        let chosen = passing[0];
        let path = if chosen.staker == agent {
            "self-stake".to_string()
        } else {
            format!("delegated by 0x{:x}", chosen.staker)
        };
        lines.push(String::new());
        lines.push(format!("Use --staker 0x{:x} on commit (or auto-detect via the skill).", chosen.staker));
        lines.push("Run `ardi-agent preflight` to confirm full readiness.".into());

        Output::success(
            lines.join("\n"),
            json!({
                "address": address_str,
                "eligible": true,
                "via": path,
                "chosen_staker": format!("0x{:x}", chosen.staker),
                "chosen_worknet_id": chosen.worknet,
                "chosen_stake_awp": chosen.stake_awp,
                "min_stake_awp": min_stake_awp,
                "all_allocations": allocs.iter().map(|a| json!({
                    "staker": format!("0x{:x}", a.staker),
                    "worknet_id": a.worknet,
                    "stake_awp": a.stake_awp,
                    "passes": a.passes,
                })).collect::<Vec<_>>(),
            }),
            Internal {
                next_action: "ready".into(),
                next_command: Some("ardi-agent preflight".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // Not eligible — print 3 paths in recommendation order. KYA first
    // (zero-AWP path, easiest); buy-and-stake second (one command for
    // anyone with ETH); manual self-stake last (existing AWP holders).
    lines.push(String::new());
    lines.push("Pick a path (in order of recommendation):".into());
    lines.push(String::new());
    lines.push("[A] 🟢 KYA delegated stake — easiest, no AWP needed".into());
    lines.push("    https://kya.link/".into());
    lines.push("    Tweet your agent address, KYA verifies on Twitter and sponsors".into());
    lines.push(format!(
        "    {} AWP into worknet {KYA_WORKNET_ID}. Wait 1-24h.",
        min_stake_awp
    ));
    lines.push(String::new());
    lines.push("[B] 🟢 One-click buy + auto-stake — for users with ETH".into());
    lines.push("    Recommended: top up ~0.01 ETH (≈ $30-40) to your agent, then run:".into());
    lines.push("        ardi-agent buy-and-stake".into());
    lines.push("    Skill quotes ETH→USDC→AWP on-chain (Uniswap V3 + Aerodrome),".into());
    lines.push("    then auto-locks into veAWP and allocates to your agent.".into());
    lines.push(format!("    Your agent address: {address_str}"));
    lines.push(String::new());
    lines.push("[C] ⚪ Manual self-stake — if you already hold AWP".into());
    lines.push("    https://awp.pro/staking".into());
    lines.push(format!(
        "    Connect wallet, lock >= {} AWP, allocate to:", min_stake_awp));
    lines.push(format!("      agent: {address_str}"));
    lines.push(format!("      worknetId: {ARDI_WORKNET_ID} (Ardi)"));
    lines.push(String::new());
    lines.push("After staking, wait ~10s, then re-run: ardi-agent stake".into());

    Output::error_with_debug(
        lines.join("\n"),
        "NOT_STAKED",
        "stake",
        false,
        &format!("Reach the {min_stake_awp} AWP threshold on EITHER Ardi (845300000014) OR KYA (845300000012) worknet, then re-run."),
        json!({
            "address": address_str,
            "eligible": false,
            "via": null,
            "ardi_worknet_id": ARDI_WORKNET_ID,
            "kya_worknet_id":  KYA_WORKNET_ID,
            "min_stake_awp":   min_stake_awp,
            "ve_awp_contract":      VE_AWP,
            "awp_allocator_contract": AWP_ALLOCATOR,
            "all_allocations": allocs.iter().map(|a| json!({
                "staker": format!("0x{:x}", a.staker),
                "worknet_id": a.worknet,
                "stake_awp": a.stake_awp,
                "passes": a.passes,
            })).collect::<Vec<_>>(),
        }),
        Internal {
            next_action: "stake_required".into(),
            next_command: Some("ardi-agent stake".into()),
            ..Default::default()
        },
    )
    .print();

    Ok(())
}
