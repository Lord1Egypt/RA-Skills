// run-loop — foreground unattended-mining daemon.
//
// `ardi-agent loop` is the no-systemd alternative to `ardi-agent auto-mine`.
// Spawns the same `tools/auto-mine/ardi-tick.sh` per tick, but in a
// foreground while-loop instead of being driven by a systemd timer.
//
// Use cases:
//   - Docker / Kubernetes containers (no systemd in PID 1)
//   - macOS (uses launchd, not systemd)
//   - Operators who'd rather see the loop in `tmux` / `screen` than
//     hunt through `journalctl`
//
// Same serial-nonce safety as the systemd path: only one tick runs at a
// time, the child process must exit before the next tick is scheduled.
// SIGINT / SIGTERM finishes the current tick (so we don't kill a child
// mid-commit) and then exits cleanly.
//
// File name is run_loop.rs — `loop` is a Rust keyword and disrupts
// `mod loop;` even with raw identifiers in some downstream tools.

use anyhow::{anyhow, Result};
use std::path::PathBuf;
use std::process::Command;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread::sleep;
use std::time::{Duration, Instant};

const DEFAULT_INTERVAL_SEC: u64 = 90;
const MIN_INTERVAL_SEC: u64 = 30;

pub struct LoopArgs {
    pub interval_sec: Option<u64>,
    pub once: bool,
}

pub fn run(args: LoopArgs) -> Result<()> {
    let interval = args
        .interval_sec
        .unwrap_or(DEFAULT_INTERVAL_SEC)
        .max(MIN_INTERVAL_SEC);

    let install_dir = resolve_install_dir()?;
    let tick = install_dir.join("ardi-tick.sh");
    if !tick.is_file() {
        return Err(anyhow!(
            "ardi-tick.sh not found at {}. Run `ardi-agent auto-mine` once to install the runtime files (it works on no-systemd hosts too — it just won't start a timer).",
            tick.display()
        ));
    }
    let env_file = std::env::var("HOME")
        .map(|h| PathBuf::from(h).join(".ardi-agent/auto-mine.env"))
        .map_err(|_| anyhow!("$HOME not set"))?;
    if !env_file.is_file() {
        eprintln!(
            "[warn] env file not found at {} — proceeding with current process env.",
            env_file.display()
        );
        eprintln!("[warn]   `ardi-agent auto-mine` writes this file on first run.");
    }

    eprintln!("[info] ardi-agent loop starting");
    eprintln!("[info]   tick:    {}", tick.display());
    eprintln!("[info]   env:     {}", env_file.display());
    eprintln!("[info]   every:   {interval}s");
    eprintln!("[info]   once:    {}", args.once);
    eprintln!("[info] press Ctrl-C to stop (current tick finishes first)");

    let stop = Arc::new(AtomicBool::new(false));
    {
        let stop = stop.clone();
        ctrlc::set_handler(move || {
            if stop.swap(true, Ordering::SeqCst) {
                // Second Ctrl-C — operator wants out NOW. Default
                // SIGINT behavior would have aborted the child too,
                // but we replaced the handler. Hard-exit the parent;
                // the child will get SIGHUP via parent death and
                // bash's job-control will shut it down.
                eprintln!("[warn] second Ctrl-C — exiting immediately");
                std::process::exit(130);
            }
            eprintln!("[info] stop requested — finishing current tick, then exiting");
        })
        .ok();
    }

    let mut tick_n: u64 = 0;
    loop {
        tick_n += 1;
        let started = Instant::now();
        eprintln!("[info] ─── tick {tick_n} ───");

        let cmd_str = format!(
            "set -a; [ -r '{env}' ] && . '{env}'; exec '{tick}'",
            env = sh_escape(env_file.to_string_lossy().as_ref()),
            tick = sh_escape(tick.to_string_lossy().as_ref()),
        );
        let status = Command::new("bash").arg("-c").arg(&cmd_str).status();

        match status {
            Ok(s) if s.success() => {
                eprintln!(
                    "[info] tick {tick_n} ok ({:.1}s)",
                    started.elapsed().as_secs_f32()
                );
            }
            Ok(s) => {
                let code = s.code().unwrap_or(-1);
                // ardi-tick.sh exit codes: 0 ok, 64/65/66 = setup
                // errors that won't resolve on retry. Surface them
                // and bail; everything else is treated as transient.
                let fatal = matches!(code, 64 | 65 | 66);
                eprintln!(
                    "[{lvl}] tick {tick_n} exited {code} ({:.1}s)",
                    started.elapsed().as_secs_f32(),
                    lvl = if fatal { "error" } else { "warn" }
                );
                if fatal {
                    return Err(anyhow!(
                        "ardi-tick.sh exited {code} (setup error). Re-run `ardi-agent auto-mine` to fix the install."
                    ));
                }
            }
            Err(e) => {
                eprintln!("[error] failed to spawn ardi-tick.sh: {e}");
            }
        }

        if args.once {
            eprintln!("[info] --once given, exiting after this tick");
            return Ok(());
        }
        if stop.load(Ordering::SeqCst) {
            eprintln!("[info] stop flag set, exiting cleanly");
            return Ok(());
        }

        // Sleep up to `interval` seconds, but wake every 1s so Ctrl-C
        // is responsive (without ctrlc-tokio integration).
        let until = Instant::now() + Duration::from_secs(interval);
        while Instant::now() < until {
            if stop.load(Ordering::SeqCst) {
                eprintln!("[info] stop flag set during sleep, exiting cleanly");
                return Ok(());
            }
            sleep(Duration::from_secs(1));
        }
    }
}

fn resolve_install_dir() -> Result<PathBuf> {
    if let Ok(p) = std::env::var("ARDI_AUTOMINE_DIR") {
        let pb = PathBuf::from(p);
        if pb.is_dir() {
            return Ok(pb);
        }
    }
    let home = std::env::var("HOME").map_err(|_| anyhow!("$HOME not set"))?;
    let installed = PathBuf::from(&home).join(".local/share/ardi-auto-mine");
    if installed.is_dir() {
        return Ok(installed);
    }
    let cloned = PathBuf::from(&home).join("ardi-skill/tools/auto-mine");
    if cloned.is_dir() {
        return Ok(cloned);
    }
    Err(anyhow!(
        "auto-mine install dir not found. Run `ardi-agent auto-mine` first to install the runtime files (it now works on no-systemd hosts: it writes the env + scripts and prints `ardi-agent loop` instructions instead of starting a timer)."
    ))
}

/// Minimal POSIX-shell single-quote escape: wrap in single quotes,
/// escape any embedded single quote as `'\''`. Safe for paths that
/// might contain spaces or shell metacharacters.
fn sh_escape(s: &str) -> String {
    s.replace('\'', "'\\''")
}
