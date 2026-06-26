// inscribe — check on-chain winners[ep][wid]; if it's us, mint via ArdiNFT.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, U256};
use alloy_sol_types::SolCall;
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::chain::{ArdiEpochDraw, ArdiNFT};
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::state::{CommitStatus, State};
use crate::tx;

pub fn run(server_url: &str, epoch_id: u64, word_id: u64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;

    // Read-only load — every state mutation in this command goes through
    // State::with_lock right before that branch returns. Concurrent
    // ticks (e.g. parallel `inscribe` calls for different (epoch,word))
    // will serialize cleanly on the per-agent flock.
    let st = State::load()?;
    let entry = match st.get(epoch_id, word_id).cloned() {
        Some(e) => e,
        None => {
            Output::error(
                format!("No local state for epoch={epoch_id} word_id={word_id}."),
                "NO_LOCAL_COMMIT",
                "state",
                false,
                "Inscribe requires a prior commit + reveal from THIS machine. \
                 If you committed elsewhere, the state file is on that machine.",
                Internal {
                    next_action: "list_state".into(),
                    next_command: Some("ardi-agent commits".into()),
                    ..Default::default()
                },
            )
            .print();
            return Ok(());
        }
    };
    if entry.status == CommitStatus::Inscribed {
        Output::success(
            format!("Already inscribed (token_id={:?}, tx={:?}).", entry.token_id, entry.inscribe_tx),
            json!({ "epoch_id": epoch_id, "word_id": word_id, "status": "inscribed" }),
            Internal {
                next_action: "done".into(),
                next_command: Some("ardi-agent commits".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }
    if matches!(entry.status, CommitStatus::Lost) {
        Output::success(
            "Already marked lost (you weren't picked as winner). Nothing to inscribe.".to_string(),
            json!({ "epoch_id": epoch_id, "word_id": word_id, "status": "lost" }),
            Internal {
                next_action: "skip".into(),
                next_command: None,
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }
    if matches!(entry.status, CommitStatus::Committed) {
        Output::error(
            "Cannot inscribe before reveal. Did you skip `reveal`?".to_string(),
            "REVEAL_FIRST",
            "state",
            false,
            format!("Run: ardi-agent reveal --epoch {epoch_id} --word-id {word_id}"),
            Internal {
                next_action: "reveal_first".into(),
                next_command: Some(format!(
                    "ardi-agent reveal --epoch {epoch_id} --word-id {word_id}"
                )),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    let api = ApiClient::new(server_url)?;
    let _ep: serde_json::Value = api.get_json(&format!("/v1/epoch/{epoch_id}"))?;
    // /v1/epoch/:id doesn't include contract addresses. Resolve via:
    //   env override → /v1/epoch/current (camelCase) → hardcoded mainnet.
    let cur_opt = api.try_get_json::<serde_json::Value>("/v1/epoch/current").ok().flatten();
    let resolve = |env_key: &str, json_key_camel: &str, json_key_snake: &str, fallback: &str| -> String {
        std::env::var(env_key).ok().or_else(|| {
            cur_opt.as_ref().and_then(|c| c.get(json_key_camel)
                .or_else(|| c.get(json_key_snake))
                .and_then(|v| v.as_str()).map(|s| s.to_string()))
        }).unwrap_or_else(|| fallback.to_string())
    };
    let draw_addr = Address::from_str(&resolve(
        "ARDI_EPOCH_DRAW_ADDR", "epochDrawContract", "epoch_draw_contract",
        "0xA57d8E6646E063FFd6eae579d4f327b689dA5DC3",
    ))?;
    let nft_addr = Address::from_str(&resolve(
        "ARDI_NFT_ADDR", "ardiNftContract", "ardi_nft_contract",
        "0xf68425D0d451699d0d766150634E436Acd2F05A1",
    ))?;

    // 1. Check on-chain winner.
    let call = ArdiEpochDraw::winnersCall {
        epochId: U256::from(epoch_id),
        wordId: U256::from(word_id),
    };
    let raw = tx::view_call(&draw_addr, call.abi_encode())?;
    if raw.len() < 32 {
        return Err(anyhow!("winners() returned <32 bytes"));
    }
    let winner = Address::from_slice(&raw[12..32]);

    if winner == Address::ZERO {
        // Disambiguate: "VRF still pending" (correct revealers exist, draw
        // is in flight) vs "your guess was wrong" (no correct revealers,
        // winner will stay 0x0 forever). Pre-v0.5.9 these were one error
        // and users wasted 16+ retries on words they'd already lost.
        let cc_call = ArdiEpochDraw::correctCountCall {
            epochId: U256::from(epoch_id),
            wordId: U256::from(word_id),
        };
        let cc_raw = tx::view_call(&draw_addr, cc_call.abi_encode())?;
        let candidates = if cc_raw.len() >= 32 {
            U256::from_be_slice(&cc_raw[..32])
        } else {
            U256::ZERO
        };

        if candidates == U256::ZERO {
            // No correct revealers — VRF will never fire for this wordId.
            // Mark Lost so `commits` stops suggesting inscribe + future
            // inscribe calls short-circuit with the right message.
            State::with_lock(|st| {
                if let Some(e) = st.get_mut(epoch_id, word_id) {
                    e.status = CommitStatus::Lost;
                }
                Ok(())
            })?;
            Output::success(
                "No correct revealers for this riddle — your answer didn't match the canonical hash. Bond was refunded on reveal; nothing more to do here.",
                json!({
                    "epoch_id": epoch_id,
                    "word_id": word_id,
                    "candidates": "0",
                    "answer_was": entry.answer,
                    "vrf_state": "no_candidate_pool",
                }),
                Internal {
                    next_action: "no_candidate_pool".into(),
                    next_command: None,
                    ..Default::default()
                },
            )
            .print();
            return Ok(());
        }

        // Real VRF wait. Base mainnet Chainlink VRF v2.5 callbacks typically
        // take 1-3 minutes (not 30s — that was a docs lie that misled every
        // tester). Worst case 8-10 min observed in the wild.
        Output::success(
            format!(
                "VRF pending — {candidates} correct revealer(s), draw in flight. Base VRF callback usually lands in 1-3 min (worst case 10 min). Retry in 60s."
            ),
            json!({
                "epoch_id": epoch_id,
                "word_id": word_id,
                "winner": "0x0",
                "candidates": candidates.to_string(),
                "vrf_state": "pending",
            }),
            Internal {
                next_action: "wait_vrf".into(),
                next_command: Some(format!(
                    "ardi-agent inscribe --epoch {epoch_id} --word-id {word_id}"
                )),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }
    if winner != agent {
        State::with_lock(|st| {
            if let Some(e) = st.get_mut(epoch_id, word_id) {
                e.status = CommitStatus::Lost;
            }
            Ok(())
        })?;
        Output::success(
            format!("Better luck next time — winner is {winner:?}, not us."),
            json!({
                "epoch_id": epoch_id,
                "word_id": word_id,
                "winner": format!("0x{:x}", winner),
                "self": agent_str,
            }),
            Internal {
                next_action: "skip".into(),
                next_command: None,
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // 2. We won — call inscribe. v3: only (epoch, wordId, word). Power +
    // language + maxDurability + element are read from EpochDraw.getAnswer
    // by the contract itself.
    let data = tx::calldata_inscribe(epoch_id, word_id, entry.answer.clone());
    let tx_obj = tx::build_tx(&agent, &nft_addr, data, 0, 350_000)?;
    let tx_hash = tx::send_and_wait(&tx_obj).context("send inscribe tx")?;

    // V3 contract: tokenId = wordId + 1 (ArdiNFTv3.sol:384). Deterministic
    // — no need to parse Inscribed event logs to learn the tokenId. Pre-v0.5.9
    // we left e.token_id = None and printed `totalInscribed` (the running
    // count, NOT the just-minted tokenId), so `commits` would later show
    // `status=inscribed token_id=null` and the success line was wrong:
    // `Ardinal #3` instead of `Ardinal #1869`. Two-line fix.
    let token_id = word_id + 1;
    let tx_hash_for_state = tx_hash.clone();
    State::with_lock(|st| {
        if let Some(e) = st.get_mut(epoch_id, word_id) {
            e.status = CommitStatus::Inscribed;
            e.inscribe_tx = Some(tx_hash_for_state);
            e.token_id = Some(token_id);
        }
        Ok(())
    })?;

    // Hand the LLM a clickable URL so the operator can verify on Basescan
    // immediately — without it, testers had to compose `cast call` to
    // confirm the mint actually landed (kaito's 2026-05-03 walkthrough,
    // friction #7). `nft_addr` is the v3 ArdiNFT proxy.
    let token_url = format!(
        "{}/token/0x{:x}/{token_id}",
        crate::cmd::commits::BASESCAN,
        nft_addr,
    );
    let tx_url = format!("{}/tx/{tx_hash}", crate::cmd::commits::BASESCAN);
    let mut data = json!({
        "epoch_id": epoch_id,
        "word_id": word_id,
        "tx_hash": tx_hash,
        "tx_url": tx_url,
        "token_id": token_id,
        "token_url": token_url,
    });
    let mut message = format!("🎉 Inscribed Ardinal #{token_id} — {token_url}");
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
            next_action: "celebrate".into(),
            next_command: Some("ardi-agent commits".into()),
            ..Default::default()
        },
    )
    .print();
    Ok(())
}
