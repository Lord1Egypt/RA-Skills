// auto-mine — install (or refresh) the unattended mining daemon.
//
// Discoverability shim. The actual installer lives in
// `tools/auto-mine/install.sh` in the public skill repo. We expose it
// as a first-class `ardi-agent auto-mine` subcommand so that LLM agents
// who only ever read `ardi-agent --help` discover the supported path
// instead of writing their own bash/python loop (which breaks the
// serial-nonce invariant and silently loses ~14 of 15 commits/epoch).
//
// Resolution order:
//   1. $ARDI_AUTOMINE_INSTALLER (env override, for testing)
//   2. ~/.local/share/ardi-auto-mine/install.sh (already installed → idempotent re-run)
//   3. ~/ardi-skill/tools/auto-mine/install.sh   (cloned alongside)
//   4. fresh `git clone` into ~/ardi-skill, then run from (3)

use anyhow::{anyhow, Result};
use serde_json::json;
use std::path::PathBuf;
use std::process::Command;

use crate::output::{Internal, Output};

const REPO_URL: &str = "https://github.com/awp-worknet/ardi-skill";

pub fn run() -> Result<()> {
    if !cfg!(target_os = "linux") {
        Output::error(
            "auto-mine daemon is Linux-only today (uses systemd user units).",
            "AUTOMINE_UNSUPPORTED_OS",
            "platform",
            false,
            "Run on a Linux host (VPS / Raspberry Pi / WSL2). On macOS / Windows, drive the cycle interactively via `ardi-agent context`.",
            Internal {
                next_action: "manual_cycle".into(),
                next_command: Some("ardi-agent context".into()),
                progress: None,
            },
        )
        .print();
        return Ok(());
    }

    let installer = resolve_installer()?;
    eprintln!("[info] running installer: {}", installer.display());

    let status = Command::new("bash")
        .arg(&installer)
        .status()
        .map_err(|e| anyhow!("failed to exec {}: {e}", installer.display()))?;

    if !status.success() {
        let code = status.code().unwrap_or(-1);
        let (suggestion, action) = match code {
            64 => (
                "No supported runtime CLI found on PATH. Install one of: claude, hermes, openclaw — then re-run `ardi-agent auto-mine`.",
                "install_runtime_cli",
            ),
            65 => (
                "ardi-agent itself is missing from PATH inside the install script's environment. Re-install ardi-agent system-wide and re-run.",
                "fix_path",
            ),
            66 => (
                // Kept for back-compat with older install.sh versions; v0.5.15+
                // installer treats no-systemd as success and recommends `ardi-agent loop`.
                "systemd not available. Use `ardi-agent loop` for foreground mode (works in Docker / containers / macOS).",
                "use_loop",
            ),
            _ => (
                "Installer failed. Re-run with bash -x for verbose output, or open an issue at github.com/awp-worknet/ardi-skill.",
                "retry",
            ),
        };
        Output::error(
            format!("auto-mine installer exited with code {code}"),
            "AUTOMINE_INSTALL_FAILED",
            "installer",
            true,
            suggestion,
            Internal {
                next_action: action.into(),
                next_command: None,
                progress: None,
            },
        )
        .print();
        return Ok(());
    }

    // The installer prints the right "next" hint for both systemd and
    // non-systemd hosts (foreground via `ardi-agent loop`). The exit
    // code is 0 in both cases — read the script's own stdout for the
    // exact follow-up command the operator should run.
    Output::success(
        "auto-mine installed. On systemd hosts a user timer is now running. \
         On no-systemd hosts (Docker / containers / macOS), run `ardi-agent loop` \
         in the foreground (or under nohup / tmux) — same pipeline, no timer needed.",
        json!({
            "installer":      installer.to_string_lossy(),
            "status_command": "~/.local/share/ardi-auto-mine/status.sh",
            "stop_command":   "~/.local/share/ardi-auto-mine/stop.sh",
            "foreground":     "ardi-agent loop",
        }),
        Internal {
            next_action: "monitor_or_run_loop".into(),
            next_command: Some("bash ~/.local/share/ardi-auto-mine/status.sh".into()),
            progress: None,
        },
    )
    .print();
    Ok(())
}

fn resolve_installer() -> Result<PathBuf> {
    if let Ok(p) = std::env::var("ARDI_AUTOMINE_INSTALLER") {
        let pb = PathBuf::from(p);
        if pb.is_file() {
            return Ok(pb);
        }
    }

    let home = std::env::var("HOME").map_err(|_| anyhow!("$HOME not set"))?;
    let installed = PathBuf::from(&home).join(".local/share/ardi-auto-mine/install.sh");
    if installed.is_file() {
        return Ok(installed);
    }

    let clone_dir = PathBuf::from(&home).join("ardi-skill");
    let cloned = clone_dir.join("tools/auto-mine/install.sh");
    if cloned.is_file() {
        eprintln!("[info] refreshing {}", clone_dir.display());
        let _ = Command::new("git")
            .arg("-C")
            .arg(&clone_dir)
            .args(["pull", "--ff-only", "--quiet"])
            .status();
        return Ok(cloned);
    }

    eprintln!("[info] cloning {REPO_URL} into {}", clone_dir.display());
    let status = Command::new("git")
        .args(["clone", "--depth", "1", REPO_URL])
        .arg(&clone_dir)
        .status()
        .map_err(|e| anyhow!("git clone failed to spawn: {e}"))?;
    if !status.success() {
        return Err(anyhow!(
            "git clone {REPO_URL} failed (exit {}). Install git and re-run, or clone manually then re-run.",
            status.code().unwrap_or(-1)
        ));
    }
    if !cloned.is_file() {
        return Err(anyhow!(
            "after clone, expected {} to exist but it does not",
            cloned.display()
        ));
    }
    Ok(cloned)
}
