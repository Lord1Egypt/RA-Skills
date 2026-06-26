// Wallet — sign + broadcast EVM txs by delegating to awp-wallet.
//
// v0.4.0: removed all private-key extraction. Previously this module
// shelled out to `awp-wallet export-private-key`, parsed the raw 32-byte
// key, and signed locally with alloy. That approach contradicted
// awp-wallet's "skill never sees, logs, or transmits private keys"
// principle and broke whenever awp-wallet shipped without that command.
//
// Now: every signing path goes through awp-wallet's own subcommands.
// Requires awp-wallet >= 1.5.0 (which introduced `send-tx` for
// arbitrary calldata). The version check at first use surfaces a clear
// error if an older awp-wallet is installed.

use anyhow::{anyhow, Context, Result};
use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

use crate::log_debug;

/// Lowest awp-wallet version that ships `send-tx` + `sign-typed-data`
/// with the JSON output shape this module parses.
const MIN_AWP_WALLET: (u32, u32, u32) = (1, 5, 0);

#[derive(Debug, Default, Clone)]
pub struct WalletStatus {
    pub cli_installed: bool,
    pub cli_path: Option<PathBuf>,
    pub wallet_dir_exists: bool,
    pub has_keystore: bool,
    pub can_receive: bool,
    pub address: Option<String>,
    pub human_status: String,
}

impl WalletStatus {
    pub fn check() -> Self {
        let mut s = Self::default();

        if let Ok(path) = which("awp-wallet") {
            s.cli_installed = true;
            s.cli_path = Some(path.clone());
            let dir = wallet_dir();
            s.wallet_dir_exists = dir.exists();
            s.has_keystore =
                dir.join("keystore.json").exists() || dir.join("wallet.json").exists();

            if let Ok(out) = Command::new(&path).arg("receive").output() {
                if out.status.success() {
                    let txt = String::from_utf8_lossy(&out.stdout);
                    if let Ok(v) = serde_json::from_str::<Value>(&txt) {
                        // awp-wallet returns {"eoaAddress":"0x..."} (current
                        // schema); older builds returned {"address":"0x..."}.
                        // Accept both.
                        if let Some(addr) = v
                            .get("eoaAddress")
                            .or_else(|| v.get("address"))
                            .and_then(|x| x.as_str())
                        {
                            s.can_receive = true;
                            s.address = Some(addr.to_lowercase());
                        }
                    }
                }
            }
        }

        s.human_status = match (s.cli_installed, s.has_keystore, s.can_receive) {
            (false, _, _) => "awp-wallet not installed".into(),
            (true, false, _) => "awp-wallet installed but no wallet — run `awp-wallet setup`".into(),
            (true, true, true) => {
                format!("awp-wallet ready; agent = {}", s.address.as_deref().unwrap_or("?"))
            }
            (true, true, false) => {
                "wallet exists but inaccessible (do NOT re-run setup — overwrites)".into()
            }
        };
        s
    }

    pub fn safe_to_init(&self) -> bool {
        !self.has_keystore
    }

    pub fn setup_command(&self) -> &'static str {
        if !self.cli_installed {
            "git clone https://github.com/awp-core/awp-wallet ~/awp-wallet && cd ~/awp-wallet && bash install.sh && awp-wallet setup"
        } else if self.safe_to_init() {
            "awp-wallet setup"
        } else {
            "(wallet already exists — do not re-init)"
        }
    }

    pub fn suggestion(&self) -> String {
        if !self.cli_installed {
            "Install awp-wallet first: `git clone https://github.com/awp-core/awp-wallet \
             ~/awp-wallet && cd ~/awp-wallet && bash install.sh && awp-wallet setup`."
                .into()
        } else if !self.has_keystore {
            "Run `awp-wallet setup` to create your wallet.".into()
        } else if !self.can_receive {
            "Wallet exists but unreadable. DO NOT run setup — that overwrites. \
             Investigate awp-wallet install."
                .into()
        } else {
            "Wallet OK.".into()
        }
    }
}

fn wallet_dir() -> PathBuf {
    let home = std::env::var("HOME").unwrap_or_else(|_| "/root".into());
    PathBuf::from(home).join(".awp-wallet")
}

fn which(bin: &str) -> Result<PathBuf> {
    if let Ok(p) = std::env::var("AWP_WALLET_BIN") {
        let pb = PathBuf::from(p);
        if pb.exists() {
            return Ok(pb);
        }
    }
    let path = std::env::var("PATH").unwrap_or_default();
    for dir in path.split(':') {
        let candidate = PathBuf::from(dir).join(bin);
        if candidate.exists() {
            return Ok(candidate);
        }
    }
    Err(anyhow!("`{bin}` not found on PATH"))
}

fn awp_wallet_bin() -> Result<PathBuf> {
    which("awp-wallet").context(
        "awp-wallet not installed. Install via: \
         `git clone https://github.com/awp-core/awp-wallet ~/awp-wallet && \
          cd ~/awp-wallet && bash install.sh && awp-wallet setup`",
    )
}

/// Read awp-wallet --version and return (major, minor, patch).
fn awp_wallet_version(bin: &PathBuf) -> Result<(u32, u32, u32)> {
    let out = Command::new(bin)
        .arg("--version")
        .output()
        .context("failed to run `awp-wallet --version`")?;
    let s = String::from_utf8_lossy(&out.stdout);
    let trimmed = s.trim();
    let parts: Vec<&str> = trimmed.split('.').collect();
    if parts.len() < 3 {
        return Err(anyhow!("unparseable awp-wallet version: '{trimmed}'"));
    }
    let parse = |p: &str| -> Result<u32> {
        p.parse::<u32>()
            .map_err(|e| anyhow!("awp-wallet version part '{p}' not numeric: {e}"))
    };
    Ok((parse(parts[0])?, parse(parts[1])?, parse(parts[2])?))
}

/// Verify awp-wallet is recent enough for the subcommands this module uses.
/// Called once at the top of every signing entry point.
fn require_min_wallet(bin: &PathBuf) -> Result<()> {
    let (a, b, c) = awp_wallet_version(bin)?;
    let (ra, rb, rc) = MIN_AWP_WALLET;
    let cur = (a, b, c);
    let req = (ra, rb, rc);
    if cur < req {
        return Err(anyhow!(
            "awp-wallet {a}.{b}.{c} too old; need >= {ra}.{rb}.{rc} \
             (introduces `send-tx` for arbitrary contract calls). \
             Upgrade: `cd ~/awp-wallet && git pull && bash install.sh`"
        ));
    }
    Ok(())
}

/// Cross-process file lock that serializes send-tx calls for the same
/// agent wallet. Without this, two `ardi-agent commit` invocations
/// fired in parallel would each fetch the same nonce from awp-wallet
/// (which itself queries the chain fresh every time) → only one tx
/// lands; the other is dropped by the node as a duplicate.
///
/// Reproduced 2026-05-03 when an LLM agent fired 15 commits in
/// parallel: 1 landed, 14 were silently lost. SKILL.md now tells
/// the LLM to commit serially, but defense-in-depth: even if it
/// doesn't, parallel calls block here instead of clashing on chain.
fn acquire_send_tx_lock() -> Result<std::fs::File> {
    use std::os::unix::io::AsRawFd;
    let dir = std::env::var("HOME").unwrap_or_else(|_| "/tmp".into());
    let path = std::path::Path::new(&dir).join(".ardi-agent").join("send-tx.lock");
    if let Some(parent) = path.parent() { let _ = std::fs::create_dir_all(parent); }
    let f = std::fs::OpenOptions::new()
        .create(true).read(true).write(true).open(&path)
        .with_context(|| format!("open send-tx lock {}", path.display()))?;
    // Blocking exclusive flock — serializes peer processes for the same
    // user. Cleared automatically when this File drops (process exit
    // or scope end).
    let rc = unsafe { libc::flock(f.as_raw_fd(), libc::LOCK_EX) };
    if rc != 0 {
        return Err(anyhow!("flock failed on {}", path.display()));
    }
    log_debug!("send-tx: acquired serialization lock {}", path.display());
    Ok(f)
}

/// Sign + broadcast an EIP-1559 transaction by delegating to
/// `awp-wallet send-tx`. Private key never enters this process.
///
/// `tx` is the same JSON shape `tx::build_tx` produces (legacy interface
/// preserved for callers). We extract the fields awp-wallet needs and
/// pass them as CLI flags. awp-wallet auto-estimates gas + maxFee + nonce
/// when omitted, but we pass through caller-supplied values to keep the
/// caller in control of the gas budget.
pub fn send_tx(tx: &Value) -> Result<String> {
    let bin = awp_wallet_bin()?;
    require_min_wallet(&bin)?;
    // Serialize parallel send-tx invocations across the user's processes
    // so they don't all grab the same chain nonce. Held until function exit.
    let _lock = acquire_send_tx_lock()?;

    // Re-fetch nonce UNDER the lock. tx::build_tx fetches nonce when it
    // composes the envelope, but that happens before this lock is held —
    // so two parallel `commit` invocations both pull nonce N from RPC,
    // then queue at this lock; the second one would broadcast with stale
    // N and the node rejects with "nonce too low: next nonce N+1, tx
    // nonce N". Reproduced 2026-05-03 by a tester firing 5 commits
    // in parallel: 1 landed, 4 lost. The lock alone wasn't enough.
    // Now: discard the caller-supplied nonce, let awp-wallet fetch
    // fresh inside the lock window (mempool has propagated by then).
    let mut tx = tx.clone();
    if let Some(obj) = tx.as_object_mut() {
        obj.remove("nonce");
    }
    let tx = &tx;

    let to = tx
        .get("to")
        .and_then(|v| v.as_str())
        .ok_or_else(|| anyhow!("tx missing `to`"))?;
    let data_hex = tx
        .get("data")
        .and_then(|v| v.as_str())
        .unwrap_or("0x");
    let value_hex = tx
        .get("value")
        .and_then(|v| v.as_str())
        .unwrap_or("0x0");
    let chain_id = tx
        .get("chainId")
        .and_then(|v| v.as_u64())
        .ok_or_else(|| anyhow!("tx missing `chainId`"))?;

    // Convert 0x-hex value/gas/nonce to decimal strings for awp-wallet's CLI.
    let value_dec = u128::from_str_radix(value_hex.trim_start_matches("0x"), 16)
        .map_err(|e| anyhow!("invalid `value` hex: {e}"))?
        .to_string();

    let mut cmd = Command::new(&bin);
    cmd.arg("--chain")
        .arg(chain_id.to_string())
        .arg("send-tx")
        .arg("--to")
        .arg(to)
        .arg("--data")
        .arg(data_hex)
        .arg("--value")
        .arg(&value_dec);

    // Pass gas + nonce if the caller supplied them; otherwise let
    // awp-wallet auto-estimate.
    if let Some(gas_hex) = tx.get("gas").and_then(|v| v.as_str()) {
        let gas = u64::from_str_radix(gas_hex.trim_start_matches("0x"), 16)
            .map_err(|e| anyhow!("invalid `gas`: {e}"))?;
        cmd.arg("--gas").arg(gas.to_string());
    }
    if let Some(nonce) = tx.get("nonce").and_then(|v| v.as_u64()) {
        cmd.arg("--nonce").arg(nonce.to_string());
    }

    log_debug!(
        "send_tx: shelling out to awp-wallet send-tx --to {to} --value {value_dec} --chain {chain_id}"
    );
    let out = cmd
        .output()
        .context("failed to invoke `awp-wallet send-tx`")?;
    let stdout = String::from_utf8_lossy(&out.stdout);
    let stderr = String::from_utf8_lossy(&out.stderr);

    if !out.status.success() {
        return Err(anyhow!(
            "awp-wallet send-tx failed (exit {:?}): {} {}",
            out.status.code(),
            stdout.trim(),
            stderr.trim()
        ));
    }

    let v: Value = serde_json::from_str(stdout.trim())
        .map_err(|e| anyhow!("awp-wallet send-tx returned non-JSON: {stdout} ({e})"))?;
    if let Some(err) = v.get("error").and_then(|e| e.as_str()) {
        return Err(anyhow!("awp-wallet send-tx reported error: {err}"));
    }
    let hash = v
        .get("txHash")
        .or_else(|| v.get("transactionHash"))
        .or_else(|| v.get("hash"))
        .and_then(|x| x.as_str())
        .ok_or_else(|| {
            anyhow!("awp-wallet send-tx response missing txHash field: {v}")
        })?
        .to_string();
    Ok(hash)
}

/// EIP-712 typed data signing — used by AWP gasless registration.
/// Delegates to `awp-wallet sign-typed-data`. Returns the 0x-prefixed
/// 65-byte signature hex.
pub fn sign_typed_data(typed_data_json: &Value) -> Result<String> {
    let bin = awp_wallet_bin()?;
    require_min_wallet(&bin)?;

    let payload = serde_json::to_string(typed_data_json)
        .map_err(|e| anyhow!("typed data serialize failed: {e}"))?;
    let out = Command::new(&bin)
        .arg("sign-typed-data")
        .arg("--data")
        .arg(&payload)
        .output()
        .context("failed to invoke `awp-wallet sign-typed-data`")?;
    let stdout = String::from_utf8_lossy(&out.stdout);
    let stderr = String::from_utf8_lossy(&out.stderr);
    if !out.status.success() {
        return Err(anyhow!(
            "awp-wallet sign-typed-data failed (exit {:?}): {} {}",
            out.status.code(),
            stdout.trim(),
            stderr.trim()
        ));
    }
    let v: Value = serde_json::from_str(stdout.trim())
        .map_err(|e| anyhow!("awp-wallet sign-typed-data returned non-JSON: {stdout} ({e})"))?;
    if let Some(err) = v.get("error").and_then(|e| e.as_str()) {
        return Err(anyhow!("awp-wallet sign-typed-data error: {err}"));
    }
    let sig = v
        .get("signature")
        .and_then(|x| x.as_str())
        .ok_or_else(|| anyhow!("awp-wallet sign-typed-data response missing signature: {v}"))?
        .to_string();
    Ok(sig)
}
