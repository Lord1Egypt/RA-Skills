// commit — sign + broadcast a commit tx for one (epoch, wordId, answer).
//
// The agent's LLM provides --word-id and --answer. We:
//   1. Generate random 32-byte salt
//   2. Compute commit_hash = keccak(answer || salt || agent)
//   3. Build commit calldata via ArdiEpochDraw::commitCall
//   4. send_tx via awp-wallet bridge with COMMIT_BOND value
//   5. Wait receipt
//   6. Persist (salt, answer) to ~/.ardi-agent/state.json so reveal can recover

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, B256, U256};
use alloy_sol_types::SolCall;
use rand::RngCore;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain;
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::state::{CommitStatus, PendingCommit, State};
use crate::tx;
use crate::{log_error, log_info};

pub struct CommitArgs {
    pub epoch_id: Option<u64>, // if None, use current
    pub word_id: u64,
    pub answer: String,
    /// v3.1: explicit staker list override. If None, auto-detect via AWP RPC.
    /// Must be unique (skill sorts strict-ascending before sending). If empty
    /// after auto-detect, hard-error so user knows to stake or fix indexer.
    pub stakers: Option<Vec<Address>>,
}

pub fn run(server_url: &str, args: CommitArgs) -> Result<()> {
    let agent_str = match get_address() {
        Ok(a) => a,
        Err(e) => {
            Output::error(
                format!("Cannot resolve agent address: {e}"),
                "WALLET_NOT_CONFIGURED",
                "dependency",
                false,
                "Run `ardi-agent preflight` to set up your wallet.",
                Internal {
                    next_action: "configure_wallet".into(),
                    next_command: Some("ardi-agent preflight".into()),
                    ..Default::default()
                },
            )
            .print();
            return Ok(());
        }
    };
    let agent = Address::from_str(&agent_str)?;

    // Resolve epoch_id from current if not given. Strong-typed deserialize:
    // any wire-format change (renamed / removed / type-shifted field)
    // surfaces as a clear `decode /v1/epoch/current: ...` error instead
    // of silently falling through .unwrap_or(0). See src/schema.rs for
    // the full spec of every external response shape.
    let api = ApiClient::new(server_url)?;
    let cur_val: Option<serde_json::Value> = api.try_get_json("/v1/epoch/current")?;
    let Some(cur_val) = cur_val else {
        Output::error(
            "No commit-able epoch right now (commit window for this cycle has closed; new epoch opens within ~6 min).",
            "NO_OPEN_EPOCH",
            "timing",
            true,
            "Wait for the next openEpoch and re-fetch with `ardi-agent context`.",
            Internal {
                next_action: "wait".into(),
                next_command: Some("ardi-agent context".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    };
    let cur: crate::schema::CurrentEpoch = crate::schema::parse("/v1/epoch/current", cur_val)?;

    let epoch_id = args.epoch_id.unwrap_or(cur.epoch_id);
    if epoch_id != cur.epoch_id {
        Output::error(
            format!("Epoch {epoch_id} is not the current commit-able epoch (current={})", cur.epoch_id),
            "WRONG_EPOCH",
            "validation",
            false,
            format!("Use --epoch {} or omit --epoch to use current.", cur.epoch_id),
            Internal {
                next_action: "fix_args".into(),
                next_command: Some(format!(
                    "ardi-agent commit --epoch {} --word-id {} --answer {}",
                    cur.epoch_id, args.word_id, args.answer
                )),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // Validate the riddle exists in the published list.
    let Some(riddle) = cur.riddles.iter().find(|r| r.word_id == args.word_id) else {
        let available: Vec<u64> = cur.riddles.iter().map(|r| r.word_id).collect();
        Output::error_with_debug(
            format!("wordId {} is not in epoch {epoch_id}'s published riddles.", args.word_id),
            "WORDID_NOT_IN_EPOCH",
            "validation",
            false,
            "Run `ardi-agent context` to see the actual wordIds for this epoch.",
            json!({ "epoch_id": epoch_id, "available_word_ids": available }),
            Internal {
                next_action: "rerun_context".into(),
                next_command: Some("ardi-agent context".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    };

    let language = riddle.language.clone();
    let language_id = riddle.language_id;
    let power = riddle.power;

    // Commit window guard — reject early instead of paying gas for a tx
    // that will revert CommitWindowClosed.
    let commit_dl = cur.commit_deadline;
    let now = chrono::Utc::now().timestamp();
    if now >= commit_dl {
        Output::error(
            format!(
                "Commit window for epoch {epoch_id} closed {}s ago. Wait for the next epoch.",
                now - commit_dl
            ),
            "COMMIT_WINDOW_CLOSED",
            "timing",
            true,
            "Wait ~6min for next openEpoch then re-fetch with `ardi-agent context`.",
            Internal {
                next_action: "wait".into(),
                next_command: Some("ardi-agent context".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // Gas + bond pre-check.
    let gas = crate::cmd::gas::check_balance(&agent_str)?;
    let need_eth = (tx::COMMIT_BOND_WEI as f64) / 1e18 + 0.0005; // bond + ~0.5mETH gas headroom
    if gas.balance_eth < need_eth {
        Output::error(
            format!(
                "Wallet has {:.6} ETH; commit needs at least {:.6} ETH (bond {} wei + gas).",
                gas.balance_eth, need_eth, tx::COMMIT_BOND_WEI
            ),
            "INSUFFICIENT_GAS",
            "balance",
            true,
            format!("Send 0.05 ETH on Base mainnet to {agent_str}, then retry."),
            Internal {
                next_action: "fund_gas".into(),
                next_command: Some("ardi-agent gas".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // Idempotency: if local state already has a commit for this (epoch,
    // word_id), don't double-commit. Same wordId from same agent in same
    // epoch would also revert AlreadyCommitted on chain.
    let st_check = State::load()?;
    if let Some(existing) = st_check.get(epoch_id, args.word_id) {
        Output::error(
            format!(
                "Already committed on (epoch={epoch_id}, word_id={}) with answer \"{}\" at tx {}.",
                args.word_id, existing.answer, existing.commit_tx
            ),
            "ALREADY_COMMITTED",
            "state",
            false,
            format!(
                "If reveal window has opened, run `ardi-agent reveal --epoch {epoch_id} --word-id {}`. \
                 To re-try with a different answer is impossible — same agent can't re-commit on the same wordId per SD-2.",
                args.word_id
            ),
            Internal {
                next_action: "skip_or_reveal".into(),
                next_command: Some(format!(
                    "ardi-agent reveal --epoch {epoch_id} --word-id {}",
                    args.word_id
                )),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // Generate nonce (was salt in v1; same role — randomness in commit hash).
    let mut nonce_bytes = [0u8; 32];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);
    let salt = B256::from(nonce_bytes);

    // v3 commit hash matches: keccak(guess || msg.sender || nonce).
    let hash = chain::commit_hash(&args.answer, &agent, &salt);
    log_info!(
        "commit: epoch={epoch_id} word={} hash=0x{}",
        args.word_id,
        hex::encode(hash)
    );

    // v3.1: resolve staker LIST. Explicit > auto-detected via AWP RPC. If
    // neither resolves we DO NOT silently fall back — H-7 fix.
    let mut stakers = match args.stakers {
        Some(s) if !s.is_empty() => s,
        _ => resolve_stakers(&api, &agent_str)?,
    };
    if stakers.is_empty() {
        Output::error(
            format!(
                "No stakers resolved for {agent_str}. Either you're not staked yet, \
                 or AWP RPC is behind. Run `ardi-agent stake` to see live chain state, \
                 then re-run with `--staker 0x... [--staker 0x...]` if you know them."
            ),
            "STAKER_NOT_RESOLVED",
            "stake",
            true,
            "Run `ardi-agent stake` and retry with --staker.",
            Internal {
                next_action: "check_stake".into(),
                next_command: Some("ardi-agent stake".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }
    // Contract requires strict ascending. Sort + dedup before sending.
    stakers.sort();
    stakers.dedup();
    if stakers.len() > 8 {
        stakers.truncate(8); // contract MAX_STAKERS_PER_COMMIT
    }
    log_info!(
        "commit: using {} staker(s): {}",
        stakers.len(),
        stakers.iter().map(|a| format!("0x{:x}", a)).collect::<Vec<_>>().join(",")
    );

    let to = Address::from_str(&cur.epoch_draw_contract)?;

    // SD-2 cap pre-flight: ArdiEpochDraw enforces maxCommitsPerEpoch (live
    // value, owner-settable; was 5 pre-2026-05-03, now 3 to align with the
    // 3-win and 3-mint caps). If the agent has already used the cap in
    // this epoch the on-chain commit reverts CommitCapReached after
    // burning gas + the bond escrow path. Catch it locally first.
    let local_in_epoch = State::load()?
        .pending
        .values()
        .filter(|c| c.epoch_id == epoch_id)
        .count();
    let live_max = read_max_commits_per_epoch(&to).unwrap_or(3) as usize;
    if local_in_epoch >= live_max {
        Output::error(
            format!(
                "Already used your {live_max}-commit cap in epoch {epoch_id} ({local_in_epoch} local commits on file). \
                 Pick the highest-EV ones and proceed to reveal after the commit window closes."
            ),
            "EPOCH_COMMIT_CAP_REACHED",
            "state",
            false,
            "Run `ardi-agent commits` to see what to reveal next, or wait for the next epoch (`ardi-agent context`).".to_string(),
            Internal {
                next_action: "wait_reveal_or_next_epoch".into(),
                next_command: Some("ardi-agent commits".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    let data = tx::calldata_commit(epoch_id, args.word_id, hash, stakers.clone());
    let tx_obj = tx::build_tx(&agent, &to, data, tx::COMMIT_BOND_WEI, 200_000)?;

    // v0.5.16 — two-phase commit save (WAL pattern).
    //
    // Pre-v0.5.16 this was a single `send_and_wait` followed by load →
    // put → save AFTER the receipt landed. That left a (small but real)
    // window between "tx mined" and "state saved" where a process kill
    // would leave a commit on chain with no local salt → reveal
    // impossible → bond forfeited.
    //
    // Now we:
    //   1. Broadcast (returns tx_hash immediately, no receipt wait)
    //   2. WAL save inside with_lock: status=Pending + the tx_hash
    //      → durable record before we block on the chain
    //   3. Wait for receipt
    //   4. Promote to Committed inside with_lock (or Failed on revert)
    //
    // The whole thing also serializes cleanly with concurrent commits
    // for OTHER (epoch, word) pairs because every state mutation is
    // inside `State::with_lock` — fixes the load-modify-save race that
    // ate commits past epoch 9 in v0.5.12 (community report 2026-05-04).
    let tx_hash = crate::wallet::send_tx(&tx_obj).context("broadcast commit tx")?;
    log_info!("commit: tx broadcast {tx_hash} (waiting receipt)");

    let answer_for_state = args.answer.clone();
    let salt_hex = format!("0x{}", hex::encode(salt));
    let commit_hash_hex = format!("0x{}", hex::encode(hash));
    let agent_str_for_state = agent_str.clone();
    let language_for_state = language.clone();
    let tx_hash_for_state = tx_hash.clone();
    State::with_lock(|st| {
        st.put(PendingCommit {
            epoch_id,
            word_id: args.word_id,
            answer: answer_for_state,
            salt_hex,
            agent: agent_str_for_state,
            commit_tx: tx_hash_for_state,
            commit_hash: commit_hash_hex,
            committed_at: chrono::Utc::now().timestamp(),
            language: language_for_state,
            power,
            language_id,
            status: CommitStatus::Pending,
            reveal_tx: None,
            inscribe_tx: None,
            token_id: None,
        });
        Ok(())
    })?;

    // Now block on the receipt. tx::wait_receipt returns (success, block).
    // On a chain revert (status != 0x1) we mark Failed so `commits` shows
    // the truth instead of leaving a stale Pending row forever.
    let (success, block) = match tx::wait_receipt(&tx_hash, 90) {
        Ok(r) => r,
        Err(e) => {
            // Receipt timed out — we don't actually know if the tx made
            // it. Leave the state at Pending; user can `cast tx <hash>`
            // to verify and re-run commit (which will see the Pending
            // entry and short-circuit the idempotency check).
            log_error!("commit: receipt wait failed for {tx_hash}: {e}");
            return Err(e).context("wait_receipt for commit");
        }
    };
    if !success {
        let tx_hash_for_fail = tx_hash.clone();
        let _ = State::with_lock(|st| {
            if let Some(e) = st.get_mut(epoch_id, args.word_id) {
                e.status = CommitStatus::Failed;
            }
            let _ = tx_hash_for_fail; // captured for the closure scope
            Ok(())
        });
        return Err(anyhow!(
            "commit tx {tx_hash} REVERTED on chain (block {block}). \
             Marked Failed locally. Common causes: CommitWindowClosed, \
             InsufficientStake, AlreadyCommitted, EpochUnknown. Decode revert: \
             cast call {to} <input> --from {agent_str} --rpc-url https://mainnet.base.org",
            to = format!("0x{:x}", to),
        ));
    }
    log_info!("commit: tx confirmed {tx_hash} (block {block})");
    State::with_lock(|st| {
        if let Some(e) = st.get_mut(epoch_id, args.word_id) {
            e.status = CommitStatus::Committed;
        }
        Ok(())
    })?;

    let mut data = json!({
        "epoch_id": epoch_id,
        "word_id": args.word_id,
        "tx_hash": tx_hash,
        "commit_hash": format!("0x{}", hex::encode(hash)),
        "bond_wei": tx::COMMIT_BOND_WEI.to_string(),
        "reveal_after": cur.commit_deadline,
    });

    let mut message = format!(
        "Commit submitted: epoch={epoch_id} word={} tx={tx_hash}. Wait until reveal window opens, then `ardi-agent reveal --epoch {epoch_id} --word-id {}`.",
        args.word_id, args.word_id
    );

    // Append a low-balance warning if the bond+gas just dropped us close.
    if let Some((warn_payload, warn_msg)) =
        crate::cmd::gas::low_balance_warning(&agent_str)
    {
        data["balance_warning"] = warn_payload;
        message = format!("{message}\n\n{warn_msg}");
    }

    Output::success(
        message,
        data,
        Internal {
            next_action: "wait_reveal".into(),
            next_command: Some(format!(
                "ardi-agent reveal --epoch {epoch_id} --word-id {}",
                args.word_id
            )),
            ..Default::default()
        },
    )
    .print();
    Ok(())
}

/// v3.1: ask AWP rootnet RPC for ALL stakers backing this agent. The
/// contract sums their allocations across BOTH worknets and accepts iff
/// total >= minStake. Returns the union of (KYA worknet stakers) +
/// (Ardi worknet stakers), filtered to non-zero allocations.
///
/// Returns empty Vec if no allocations found anywhere; caller hard-errors.
/// Source of truth is on chain (`AWPAllocator.getAgentStake` at commit) —
/// stale RPC just means commit reverts.
/// Read the live `maxCommitsPerEpoch` from the EpochDraw contract.
/// Owner can change this without redeploy (e.g. 5→3 on 2026-05-03 to
/// align commit cap with the 3-win / 3-mint caps), so the skill must
/// not hardcode it. Returns None on any RPC failure — caller falls
/// back to a conservative default of 3.
fn read_max_commits_per_epoch(epoch_draw_addr: &Address) -> Option<u8> {
    let raw = tx::view_call(
        epoch_draw_addr,
        chain::ArdiEpochDraw::maxCommitsPerEpochCall {}.abi_encode(),
    )
    .ok()?;
    if raw.len() < 32 { return None; }
    Some(raw[31])
}

fn resolve_stakers(_api: &ApiClient, agent_addr: &str) -> Result<Vec<Address>> {
    // Verified against AWP subnets.get on 2026-05-02:
    //   845300000014 = ARDI Worknet (self-stake lives here)
    //   845300000012 = KYA  Worknet (delegated stakes land here)
    const ARDI_WN: &str = "845300000014";
    const KYA_WN: &str = "845300000012";

    let rpc = crate::awp_rpc::AwpRpc::new()?;

    use std::collections::BTreeSet;
    let mut set: BTreeSet<Address> = BTreeSet::new();
    for wn in [KYA_WN, ARDI_WN] {
        if let Ok(rows) = rpc.allocations_by_agent_worknet(agent_addr, wn, None) {
            for row in rows {
                let amount = U256::from_str_radix(&row.amount, 10).unwrap_or(U256::ZERO);
                if amount == U256::ZERO { continue; }
                if let Ok(addr) = Address::from_str(&row.user_address) {
                    set.insert(addr);
                }
            }
        }
    }
    Ok(set.into_iter().collect()) // BTreeSet → ascending Vec, naturally sorted+deduped
}
