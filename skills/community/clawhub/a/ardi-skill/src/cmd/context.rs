// context — fetch the current commit-able epoch + riddles from coord-rs.

use anyhow::Result;
use serde_json::json;

use crate::client::ApiClient;
use crate::output::{Internal, Output};

pub fn run(server_url: &str) -> Result<()> {
    let api = ApiClient::new(server_url)?;
    let body: Option<serde_json::Value> = api.try_get_json("/v1/epoch/current")?;
    match body {
        Some(raw) => {
            // Parse strict-typed first; fall back to passing the raw JSON
            // through so the LLM still gets the riddles even if a new
            // optional field gets added that we don't know about.
            let parsed: crate::schema::CurrentEpoch =
                crate::schema::parse("/v1/epoch/current", raw.clone())?;
            let now = chrono::Utc::now().timestamp();
            let secs_left = parsed.commit_deadline - now;
            let mut message = format!(
                "Epoch {}: commit window closes in {secs_left}s ({} riddles).",
                parsed.epoch_id, parsed.riddles.len()
            );
            // Echo the raw payload so the LLM sees every field including
            // theme/element + any future additions (it's the agent's
            // input for solving). We tack a balance_warning onto it.
            let mut epoch = raw;
            if let Ok(addr) = crate::auth::get_address() {
                if let Some((warn_payload, warn_msg)) =
                    crate::cmd::gas::low_balance_warning(&addr)
                {
                    if let serde_json::Value::Object(ref mut m) = epoch {
                        m.insert("balance_warning".into(), warn_payload);
                    }
                    message = format!("{message}\n\n{warn_msg}");
                }
            }
            Output::success(
                message,
                epoch,
                Internal {
                    next_action: "solve_then_commit".into(),
                    next_command: Some(
                        "ardi-agent commit --word-id <ID> --answer \"<your answer>\"".into(),
                    ),
                    ..Default::default()
                },
            )
            .print();
        }
        None => {
            Output::success(
                "No epoch is currently in commit window. Wait for the next openEpoch (~6 min cycle).",
                json!({ "current": null }),
                Internal {
                    next_action: "wait".into(),
                    next_command: Some("ardi-agent context".into()),
                    ..Default::default()
                },
            )
            .print();
        }
    }
    Ok(())
}
