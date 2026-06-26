---
name: clever-compact
description: "Your OpenClaw agent forgets everything between sessions — after /new, after compaction, after overnight. Clever Compact fixes all three: injects your last state on session start, flushes before every compact, and keeps memory stable across context resets. Native plugin. Zero per-turn overhead. Install in 4 steps, runs automatically."
---

# Clever Compact

**Publisher:** AxiomStream Group  
**Version:** 2.2.5  
**Tier:** Free  
**ClaWHub:** https://clawhub.ai/jfulmines-star/clever-compact  
**Support:** kit@axiomstreamgroup.com

---

## What This Skill Does

Clever Compact fixes the three memory failure modes every serious OpenClaw user hits:

- **`/new` amnesia** — fresh session, agent acts like it's never met you
- **Compaction loss** — context fills up, compact fires, agent forgets what it was doing mid-task
- **Overnight drift** — decisions from three sessions ago quietly disappear

**v2 is a native OpenClaw plugin** with two parts:

**Session restore (automatic):** At the start of every session — including after `/new` and after compaction — Clever Compact checks for a recent compact-state file. If one exists (written within 72 hours), it injects the content as system context on the **first turn only**. Your agent wakes up oriented with zero per-turn token overhead.

**State write (triggered by you):** OpenClaw doesn't expose a pre-compaction lifecycle hook yet, so the write side is explicit — not automatic. Three ways to trigger it; pick one (see below).

---

## Installation (4 steps)

**1. Install:**
```bash
openclaw skills add https://clawhub.ai/jfulmines-star/clever-compact
```

**2. Enable in `~/.openclaw/openclaw.json`:**
```json
{
  "plugins": {
    "entries": {
      "clever-compact": {
        "enabled": true
      }
    }
  }
}
```

**3. Add to `plugins.allow`:**
```json
{
  "plugins": {
    "allow": ["clever-compact"]
  }
}
```

**4. Restart gateway:**
```bash
openclaw gateway restart
```

That's it. Session restore is now active automatically.

---

## Writing State

Pick one trigger method:

**Manual** — Tell your agent:
> "Run a Clever Compact flush"

**Heartbeat** — Add to your `HEARTBEAT.md`:
```markdown
## Context Flush (at >75% context)
- Run a Clever Compact flush — write state to memory/compact-state-YYYY-MM-DD-HHmm.md
```

**Cron** — Schedule a pre-compact flush via Piston or system cron, 5 minutes before your nightly compact:
```
Payload: "Pre-compaction memory flush. Store durable memories now."
```

The plugin also exposes `api.fn("clever-compact:write")` for programmatic triggers from other tools.

---

## Using with memory-core (IMPORTANT — OC 2026.5.2+)

If you're running both Clever Compact and memory-core, you have two great tools that do different things — and they work together perfectly when configured correctly.

**What each owns:**
- **Clever Compact** → cross-session state injection (compact-state files → session start restore)
- **memory-core** → within-session memory flush, `memory_search`/`memory_get` tools, dreaming

**The conflict:** On OC 2026.5.2+, both plugins can fire a session-start injection at the same time. The fix is one config line.

**Recommended config (both enabled, no conflict):**

```json
"plugins": {
  "entries": {
    "clever-compact": {
      "enabled": true
    },
    "memory-core": {
      "enabled": true,
      "config": {
        "memoryFlush": {
          "enabled": false
        }
      }
    }
  }
}
```

With this setup: memory-core handles search tools and dreaming, Clever Compact handles session restore. No overlap, no conflict.

**Advanced:** If you want memory-core's flush AND CC's session restore, set both enabled but point memory-core's flush to a different target file. Most users don't need this — the config above covers 99% of setups.

---

## Compatibility

| Version | Status |
|---|---|
| OpenClaw 2026.4.10+ | ✅ Supported |
| OpenClaw 2026.5.2+ | ✅ Supported (use memory-core config above if both enabled) |
| OpenClaw < 2026.4.10 | ❌ Not supported |

---

## Changelog

- **v2.2.4** — Fix: session flag now scoped per-registration (fixes blank-session bug on OC 2026.5.2 plugin loading changes). Added memory-core coexistence guidance.
- **v2.2.3** — Stable release. Version sync across package files.
- **v2.2.0** — Native plugin (no longer skill-only). Injects once per session only — eliminates per-turn token overhead.

---

*Built by AxiomStream Group — axiomstreamgroup.com*  
*We built this because we needed it. We run it on our own agents every day.*

---

⭐ **If Clever Compact saved your agent's memory, star it on ClaWHub** — it helps other users find it and tells us the fix was worth shipping.
[Star on ClaWHub →](https://clawhub.ai/jfulmines-star/clever-compact)

---

## Security

Clever Compact is a memory plugin. It reads and writes local files in your `OPENCLAW_WORKSPACE/memory/` directory only. No network requests, no shell execution, no credential access.

The ClawHub security scanner flags memory plugins because they use `fs`, `process.env`, `before_prompt_build`, and `prependSystemContext` — the same capabilities used by OpenClaw's own `memory-core` plugin. These are required for any memory plugin to function.

See [`SECURITY.md`](./SECURITY.md) for the full capability-by-capability breakdown, or [GitHub issue #1989](https://github.com/openclaw/clawhub/issues/1989) for the false-positive report.

VirusTotal: ✅ Benign | Static analysis: ✅ Benign | ClawScan: 🔄 Under review
