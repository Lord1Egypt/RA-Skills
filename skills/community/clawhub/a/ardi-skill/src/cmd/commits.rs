// commits — list local pending commits + per-row next_command.
//
// This is what an agent calls between rounds to figure out "what should I
// do next?" — it surfaces commits that need reveal (window open) or
// inscribe (winner picked).

use std::collections::HashMap;
use std::str::FromStr;

use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use anyhow::Result;
use serde_json::json;

use crate::chain::ArdiEpochDraw;
use crate::output::{Internal, Output};
use crate::state::{CommitStatus, State};
use crate::tx;

pub const BASESCAN: &str = "https://basescan.org";
// Reveal becomes valid 30s after commitDeadline — gives the coordinator
// time to land publishAnswers() on chain. Going earlier returns
// REVEAL_TX_FAILED. Tester reported in 2026-05-03 walkthrough that they
// had to "guess by stopwatch" — this surfaces the timestamp explicitly.
const REVEAL_PUBLISH_GRACE_SEC: u64 = 30;

fn tx_url(hash: &str) -> String { format!("{BASESCAN}/tx/{hash}") }
fn token_url(nft_addr: &str, token_id: u64) -> String {
    format!("{BASESCAN}/token/{nft_addr}/{token_id}")
}

pub fn run(_server_url: &str) -> Result<()> {
    let now = chrono::Utc::now().timestamp();

    // Backfill: any Inscribed/Won row that's missing token_id was written by
    // pre-v0.5.9 inscribe (which never recorded the tokenId). V3 derives
    // tokenId = wordId + 1 deterministically, so we can repair retroactively
    // without an RPC call. This eliminates the "ardi-agent commits says
    // token_id:null but ardi-agent status / chain says #1869 is mine" lie
    // that misled testers into thinking they hadn't won.
    //
    // Wrap in `with_lock` so a concurrent commit/reveal/inscribe doesn't
    // race the backfill write. The closure no-ops on its way out if no
    // rows needed repair, so the lock cost on every `commits` call is
    // just one fsync's worth.
    let st = State::with_lock(|st| {
        let mut backfilled = 0;
        for c in st.pending.values_mut() {
            if matches!(c.status, CommitStatus::Inscribed | CommitStatus::Won) && c.token_id.is_none() {
                c.token_id = Some(c.word_id + 1);
                backfilled += 1;
            }
        }
        let _ = backfilled; // tracked only for symmetry with prior log line
        Ok(st.clone())
    })?;

    // Pre-fetch commitDeadline for each epoch with at least one Committed
    // row, so we can surface `next_reveal_eligible_at` (= commitDeadline +
    // 30s publish grace). One eth_call per distinct epoch — usually 1-2
    // because users batch within a round.
    let nft_addr = std::env::var("ARDI_NFT_ADDR")
        .unwrap_or_else(|_| "0xf68425D0d451699d0d766150634E436Acd2F05A1".to_string());
    let draw_addr_str = std::env::var("ARDI_EPOCH_DRAW_ADDR")
        .unwrap_or_else(|_| "0xA57d8E6646E063FFd6eae579d4f327b689dA5DC3".to_string());
    let mut deadline_by_epoch: HashMap<u64, u64> = HashMap::new();
    if let Ok(draw_addr) = Address::from_str(&draw_addr_str) {
        let pending_epochs: std::collections::BTreeSet<u64> = st
            .pending
            .values()
            .filter(|c| matches!(c.status, CommitStatus::Committed))
            .map(|c| c.epoch_id)
            .collect();
        for ep in pending_epochs {
            let call = ArdiEpochDraw::epochsCall { epochId: U256::from(ep) };
            // Best-effort — RPC blip shouldn't break the listing.
            if let Ok(raw) = tx::view_call(&draw_addr, call.abi_encode()) {
                if raw.len() >= 64 {
                    // tuple is (uint64 startTs, uint64 commitDeadline, ...);
                    // each uint64 sits right-aligned in a 32-byte word.
                    let bytes: [u8; 8] = raw[56..64].try_into().unwrap_or([0u8; 8]);
                    let commit_deadline = u64::from_be_bytes(bytes);
                    deadline_by_epoch.insert(ep, commit_deadline);
                }
            }
        }
    }

    let mut rows: Vec<serde_json::Value> = Vec::new();
    for c in st.pending.values() {
        let suggested_next = match c.status {
            CommitStatus::Committed => Some(format!(
                "ardi-agent reveal --epoch {} --word-id {} (after commit_deadline + publish)",
                c.epoch_id, c.word_id
            )),
            CommitStatus::Revealed => Some(format!(
                "ardi-agent inscribe --epoch {} --word-id {}",
                c.epoch_id, c.word_id
            )),
            CommitStatus::Won => Some(format!(
                "ardi-agent inscribe --epoch {} --word-id {}",
                c.epoch_id, c.word_id
            )),
            _ => None,
        };

        let mut row = json!({
            "epoch_id": c.epoch_id,
            "word_id": c.word_id,
            "status": format!("{:?}", c.status).to_lowercase(),
            "answer": c.answer,
            "committed_at": c.committed_at,
            "age_seconds": now - c.committed_at,
            "commit_tx": c.commit_tx,
            "commit_tx_url": tx_url(&c.commit_tx),
            "reveal_tx": c.reveal_tx,
            "reveal_tx_url": c.reveal_tx.as_ref().map(|h| tx_url(h)),
            "inscribe_tx": c.inscribe_tx,
            "inscribe_tx_url": c.inscribe_tx.as_ref().map(|h| tx_url(h)),
            "token_id": c.token_id,
            "token_url": c.token_id.map(|t| token_url(&nft_addr, t)),
            "next_command": suggested_next,
        });

        // Surface the timestamp the LLM should sleep until before calling
        // reveal — eliminates the "wait, when can I reveal?" guesswork.
        if matches!(c.status, CommitStatus::Committed) {
            if let Some(dl) = deadline_by_epoch.get(&c.epoch_id) {
                let eligible_at = dl + REVEAL_PUBLISH_GRACE_SEC;
                row["next_reveal_eligible_at"] = json!(eligible_at);
                let secs_left = (eligible_at as i64) - now;
                if secs_left > 0 {
                    row["next_reveal_in_seconds"] = json!(secs_left);
                } else {
                    row["next_reveal_in_seconds"] = json!(0);
                }
            }
        }

        rows.push(row);
    }

    let next_action = if rows
        .iter()
        .any(|r| r.get("status").and_then(|v| v.as_str()) == Some("revealed"))
    {
        "inscribe_pending"
    } else if rows
        .iter()
        .any(|r| r.get("status").and_then(|v| v.as_str()) == Some("committed"))
    {
        "reveal_pending"
    } else {
        "idle"
    };

    let mut data = json!({ "pending": rows });
    let mut message = format!("{} pending commits ({})", rows.len(), next_action);

    // Wallet balance reminder — agents tend to forget topping up.
    if let Ok(addr) = crate::auth::get_address() {
        if let Some((warn_payload, warn_msg)) = crate::cmd::gas::low_balance_warning(&addr) {
            data["balance_warning"] = warn_payload;
            message = format!("{message}\n\n{warn_msg}");
        }
    }

    Output::success(
        message,
        data,
        Internal {
            next_action: next_action.into(),
            next_command: rows
                .iter()
                .find_map(|r| r.get("next_command").and_then(|v| v.as_str()))
                .map(String::from),
            ..Default::default()
        },
    )
    .print();
    Ok(())
}
