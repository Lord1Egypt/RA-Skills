// Local state — tracks pending commits per agent.
//
// A commit on chain only carries hash(answer, salt, agent). To reveal we
// need to remember the plaintext (answer, salt) we committed with. Stored
// at ~/.ardi-agent/state-<addr>.json, owned by the user (no daemon, no
// rotation).
//
// v0.5.16 — concurrency hardening
// ───────────────────────────────
// Earlier versions exposed `State::load()` / `State::save()` directly,
// which let two parallel `ardi-agent commit` invocations race the
// classic load-modify-save:
//
//   A: load() -> {e9: A_old}
//   B: load() -> {e9: A_old}
//   A: put(e10: A_new); save() -> writes {e9, e10:A_new}
//   B: put(e10: B_new); save() -> writes {e9, e10:B_new}   ← A_new lost
//
// External report (community user, v0.5.12): "commits submit on-chain
// successfully but state doesn't update after epoch 9". The lost-write
// pattern reproduces this exactly — A's commit lands on chain, but the
// local salt/answer is gone, so the subsequent `reveal` can't find the
// pre-image and forfeits the bond.
//
// Fix: every load-modify-save MUST go through `State::with_lock` which
// takes an exclusive flock on `~/.ardi-agent/state-<addr>.lock` for the
// entire load → mutate → save window. flock is advisory but every code
// path in this binary cooperates. Stale locks aren't possible — the OS
// drops the flock when the process exits.

use anyhow::{Context, Result};
use fs2::FileExt;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::fs::{self, File, OpenOptions};
use std::path::PathBuf;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PendingCommit {
    pub epoch_id: u64,
    pub word_id: u64,
    pub answer: String,
    pub salt_hex: String,        // 0x-prefixed 32-byte hex
    pub agent: String,           // 0x-lower
    pub commit_tx: String,       // 0x hash
    pub commit_hash: String,     // 0x bytes32 we computed
    pub committed_at: i64,       // unix seconds
    pub language: String,
    pub power: u16,
    pub language_id: u8,
    pub status: CommitStatus,
    pub reveal_tx: Option<String>,
    pub inscribe_tx: Option<String>,
    pub token_id: Option<u64>,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum CommitStatus {
    /// v0.5.16 WAL state: salt + answer persisted to disk BEFORE the tx
    /// is broadcast. Eliminates the broadcast-then-crash window where
    /// the tx lands on chain but the local salt is lost. Promoted to
    /// `Committed` once the receipt confirms `status == 0x1`.
    /// Old states with no `Pending` field default to `Committed` on
    /// load — no migration needed.
    Pending,
    Committed,
    Revealed,
    /// VRF picked us as winner; ready to inscribe.
    Won,
    /// VRF picked someone else; nothing more to do.
    Lost,
    /// Already minted into ArdiNFT.
    Inscribed,
    /// Anything that went wrong — kept for debugging.
    Failed,
}

#[derive(Serialize, Deserialize, Default, Debug, Clone)]
pub struct State {
    /// Keyed "{epoch_id}:{word_id}" so it round-trips JSON cleanly.
    #[serde(default)]
    pub pending: BTreeMap<String, PendingCommit>,
}

impl State {
    /// Read-only load. Safe to use for read paths (`commits` listing,
    /// `reveal` lookup) — the read-modify-write paths must use
    /// `with_lock` instead so they don't race other writers.
    pub fn load() -> Result<Self> {
        let p = path();
        if !p.exists() {
            return Ok(Self::default());
        }
        let raw = fs::read_to_string(&p)
            .with_context(|| format!("read {}", p.display()))?;
        let s = serde_json::from_str(&raw).unwrap_or_default();
        Ok(s)
    }

    /// Atomic load → mutate → save under an exclusive flock. The lock
    /// covers the entire critical section, so two concurrent
    /// `with_lock` callers serialize cleanly.
    ///
    /// The lock file is `~/.ardi-agent/state-<addr>.lock`; the process
    /// holds it only for the duration of the closure (≪ 1ms typically),
    /// and the OS releases it on exit even if the closure panics.
    ///
    /// ⚠ Do NOT call `with_lock` from inside another `with_lock` — the
    /// flock is exclusive and you'll self-deadlock. Same goes for
    /// calling chain RPC inside the closure: keep the critical section
    /// short. Build the new PendingCommit value outside, then `put` it
    /// inside.
    pub fn with_lock<F, R>(f: F) -> Result<R>
    where
        F: FnOnce(&mut State) -> Result<R>,
    {
        let p = path();
        if let Some(dir) = p.parent() {
            fs::create_dir_all(dir).ok();
        }
        let lock_path = p.with_extension("lock");
        let lock_file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .open(&lock_path)
            .with_context(|| format!("open lock file {}", lock_path.display()))?;
        // Block until we own the lock. We'd rather queue than fail —
        // contention is brief because the closure is just JSON I/O.
        FileExt::lock_exclusive(&lock_file)
            .with_context(|| format!("flock {}", lock_path.display()))?;
        // RAII: release the lock no matter how the closure exits
        // (success / Err / panic). Drop order: result then guard.
        struct LockGuard(File);
        impl Drop for LockGuard {
            fn drop(&mut self) {
                let _ = FileExt::unlock(&self.0);
            }
        }
        let _guard = LockGuard(lock_file);

        let mut state = Self::load()?;
        let r = f(&mut state)?;
        state.save_inner(&p)?;
        Ok(r)
    }

    /// Atomic write — temp file + rename. Renamed inside the lock by
    /// `with_lock`; do not call directly from outside the module.
    fn save_inner(&self, p: &PathBuf) -> Result<()> {
        let tmp = p.with_extension("json.tmp");
        fs::write(&tmp, serde_json::to_string_pretty(self)?)?;
        fs::rename(&tmp, p)?;
        Ok(())
    }

    pub fn key(epoch_id: u64, word_id: u64) -> String {
        format!("{epoch_id}:{word_id}")
    }

    pub fn put(&mut self, c: PendingCommit) {
        self.pending.insert(Self::key(c.epoch_id, c.word_id), c);
    }

    pub fn get(&self, epoch_id: u64, word_id: u64) -> Option<&PendingCommit> {
        self.pending.get(&Self::key(epoch_id, word_id))
    }

    pub fn get_mut(&mut self, epoch_id: u64, word_id: u64) -> Option<&mut PendingCommit> {
        self.pending.get_mut(&Self::key(epoch_id, word_id))
    }
}

/// Per-agent state file path. Each agent address gets its own file so two
/// wallets on the same machine never clash. Falls back to `state.json` when
/// no address resolved yet (preflight not yet run).
fn path() -> PathBuf {
    let home = std::env::var("HOME").unwrap_or_else(|_| "/root".into());
    let dir = PathBuf::from(home).join(".ardi-agent");
    let addr = crate::auth::get_address().ok();
    let fname = match addr {
        Some(a) => format!("state-{}.json", a.to_lowercase()),
        None => "state.json".to_string(),
    };
    dir.join(fname)
}
