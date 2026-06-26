// reveal — submit reveal for one (epoch, wordId). Pulls salt + answer from
// local state, asks server for the vault Merkle proof, sends reveal tx.

use anyhow::{anyhow, Context, Result};
use alloy_primitives::{Address, B256};
use serde_json::json;
use std::str::FromStr;

use crate::auth::get_address;
use crate::client::ApiClient;
use crate::output::{Internal, Output};
use crate::state::{CommitStatus, State};
use crate::tx;
use crate::log_info;

pub fn run(server_url: &str, epoch_id: u64, word_id: u64) -> Result<()> {
    let agent_str = get_address()?;
    let agent = Address::from_str(&agent_str)?;

    // Read-only load — we only mutate state at the end (after tx
    // confirms), and that mutation goes through State::with_lock.
    let st = State::load()?;
    let entry = match st.get(epoch_id, word_id).cloned() {
        Some(e) => e,
        None => {
            Output::error(
                format!("No local state for epoch={epoch_id} word_id={word_id}."),
                "NO_LOCAL_COMMIT",
                "state",
                false,
                "Did you commit first? `ardi-agent commits` lists what we have. \
                 If you committed from a different machine, the salt is lost \
                 and reveal cannot be reconstructed — bond will be forfeited.",
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
    if entry.status != CommitStatus::Committed {
        Output::error(
            format!("Status is {:?}, not committed — nothing to reveal.", entry.status),
            "WRONG_STATUS_FOR_REVEAL",
            "state",
            false,
            match entry.status {
                CommitStatus::Revealed => "Already revealed. Try `ardi-agent inscribe` next.".to_string(),
                CommitStatus::Inscribed => "Already inscribed. See `ardi-agent commits` for full state.".to_string(),
                CommitStatus::Lost => "VRF picked another winner — nothing more to do.".to_string(),
                _ => "Run `ardi-agent commits` to see full local state.".to_string(),
            },
            Internal {
                next_action: "review_state".into(),
                next_command: Some("ardi-agent commits".into()),
                ..Default::default()
            },
        )
        .print();
        return Ok(());
    }

    // v3 reveal needs only (guess, nonce). Vault proof was a v1/v2 artifact —
    // those proofs are checked server-side in publishAnswers, not by reveal.
    let api = ApiClient::new(server_url)?;

    let salt_bytes = hex::decode(entry.salt_hex.trim_start_matches("0x"))
        .context("invalid salt in state — file corrupted?")?;
    if salt_bytes.len() != 32 {
        return Err(anyhow!("salt has wrong length"));
    }
    let nonce = B256::from_slice(&salt_bytes);

    // Fetch contract addr (and check reveal window) from current epoch row.
    let ep: serde_json::Value = api.get_json(&format!("/v1/epoch/{epoch_id}"))?;
    // /v1/epoch/:id doesn't return contract addresses (snake_case OR
    // camelCase); we resolve via env var override → /v1/epoch/current
    // (which DOES return epochDrawContract) → hardcoded mainnet default.
    let resolved = std::env::var("ARDI_EPOCH_DRAW_ADDR").ok().or_else(|| {
        api.try_get_json::<serde_json::Value>("/v1/epoch/current")
            .ok().flatten()
            .and_then(|c| c.get("epochDrawContract").or_else(|| c.get("epoch_draw_contract"))
                .and_then(|v| v.as_str()).map(|s| s.to_string()))
    }).unwrap_or_else(|| "0xA57d8E6646E063FFd6eae579d4f327b689dA5DC3".to_string());
    let to = match Address::from_str(&resolved) {
        Ok(a) => a,
        Err(_) => {
            Output::error(
                "Could not resolve EpochDraw contract address.",
                "SERVER_MISSING_CONTRACT_ADDR",
                "server",
                false,
                "Set ARDI_EPOCH_DRAW_ADDR env to override (mainnet default 0x21c2ebA5...).",
                Internal { next_action: "blocked".into(), ..Default::default() },
            )
            .print();
            return Ok(());
        }
    };

    let data = tx::calldata_reveal(epoch_id, word_id, entry.answer.clone(), nonce);
    let tx_obj = tx::build_tx(&agent, &to, data, 0, 250_000)?;
    let tx_hash = match tx::send_and_wait(&tx_obj) {
        Ok(h) => h,
        Err(e) => {
            Output::error(
                format!("Reveal tx broadcast failed: {e}"),
                "REVEAL_TX_FAILED",
                "chain",
                true,
                "Common causes: (a) reveal window not yet open — server hasn't called publishAnswers; (b) tx underpriced; (c) RPC hiccup. Wait 30s then retry.",
                Internal {
                    next_action: "retry_later".into(),
                    next_command: Some(format!(
                        "ardi-agent reveal --epoch {epoch_id} --word-id {word_id}"
                    )),
                    ..Default::default()
                },
            )
            .print();
            return Ok(());
        }
    };
    log_info!("reveal: tx submitted {tx_hash}");

    // Atomic state update under flock — concurrent ticks (e.g. another
    // reveal in the same auto-mine cycle) won't lose this write.
    let tx_hash_for_state = tx_hash.clone();
    State::with_lock(|st| {
        if let Some(e) = st.get_mut(epoch_id, word_id) {
            e.status = CommitStatus::Revealed;
            e.reveal_tx = Some(tx_hash_for_state);
        }
        Ok(())
    })?;

    let mut data = json!({
        "epoch_id": epoch_id,
        "word_id": word_id,
        "tx_hash": tx_hash,
    });
    let mut message = format!(
        "Reveal submitted: epoch={epoch_id} word={word_id} tx={tx_hash}. \
         Wait for VRF (~30s after request_draw), then run inscribe."
    );
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
            next_action: "wait_vrf_then_inscribe".into(),
            next_command: Some(format!(
                "ardi-agent inscribe --epoch {epoch_id} --word-id {word_id}"
            )),
            ..Default::default()
        },
    )
    .print();
    Ok(())
}
