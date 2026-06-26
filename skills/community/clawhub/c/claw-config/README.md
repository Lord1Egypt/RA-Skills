# claw-config

Shared skill for the OpenClaw self-hosted agent gateway that lets any single agent safely self-diagnose and self-modify its own slice of `~/.openclaw/openclaw.json` without hallucinating field names, identity, or paths.

Python 3 · stdlib only · MIT

---

## The Problem

Even with frontier models driving them, OpenClaw agents hallucinate when asked to modify their own config:

1. **They don't know who they are.** Which entry in `agents.list[]` is their own identity?
2. **They invent field names.** Writing `nativeSkill` or `enableSkills` from training memory when the real name is `commands.nativeSkills`.
3. **They don't know what fields do.** `--help` and schema descriptions are sparse; real semantics live in prose docs.
4. **Docs they remember may be stale.** The docs they recall from training are out of date vs. the binary they're running against.
5. **They can edit another agent's slice.** The highest-impact failure mode.

A production incident illustrated this: an agent's `commands.nativeSkills` was silently set to `false` on its Telegram account, which hid its workspace skills from chat dispatch. The agent couldn't self-diagnose because `--help` didn't describe the field and the schema only said `boolean | "auto"`. A human had to debug it.

**`claw-config`** exists to prevent that failure mode.

---

## Design Principles

Seven design choices, each a defense against a specific hallucination mode:

### 1. No LLM in the loop for facts

Every field name, current value, and JSON pointer is read at call time from the installed `openclaw` CLI (`openclaw config schema`, `openclaw config get`) — never from the model's training memory.

### 2. Identity is required, never guessed

Resolves `$OPENCLAW_AGENT_ID` → `--agent <id>` flag → otherwise `exit 2`. The skill refuses to infer identity from `cwd`, hostname, or first-in-list. Wrong-agent writes are impossible by construction.

### 3. Cross-agent writes are statically refused

`plan` and `apply` walk the patch and reject any reference to another agent's slice (`channels.<chan>.accounts.<other>`, `agents.list[i].id != self`).

### 4. Official docs are first-class

Built-in `docs <topic>` and `docs search:<keyword>` subcommands fetch raw markdown from `docs.openclaw.ai` (Mintlify `.md` endpoints + the full-content `llms-full.txt` corpus). Use this **before** composing any patch.

### 5. Cache is version-keyed

Docs cache lives under `~/.openclaw/.maintenance-cache/docs/<openclaw-version>/<slug>`. When the user upgrades openclaw, the previous version's cache directory is auto-removed on the next docs call. Each call reports cache age on stderr so the caller can decide to `--refresh`.

### 6. Writes go through `openclaw config patch`

No hand-edited JSON. Patches are JSON5 with recursive merge semantics (null deletes, arrays/scalars replace). The CLI validates against schema internally before writing. Versioned backups in a dedicated directory (avoids being caught by openclaw's own rotating-backup cleanup) with automatic rollback on failure.

### 7. Schema is truth, docs are guidance

`docs.openclaw.ai` always reflects the latest published openclaw release; the installed binary may lag (stable channel) or lead (dev channel). When they disagree, trust schema (it comes from the installed binary). This is documented in SKILL.md so calling agents know.

---

## Subcommands

| Command | Purpose | Writes? | Cron-safe? |
|---|---|---|---|
| `claw-config whoami [--json]` | Agent record + telegram flags + bindings + cron jobs + skills inventory | No | Yes |
| `claw-config schema [<pointer>]` | JSON schema (or sub-tree) from installed binary | No | Yes |
| `claw-config docs [<topic>\|search:<kw>] [--refresh] [--max-age <h>]` | Official documentation as raw markdown, per-version cache | No (writes cache) | Yes (cache-only in cron) |
| `claw-config diagnose [--json]` | 12 structural self-checks; exits 3 on any fail | No | Yes |
| `claw-config plan <patch.json5>` | Dry-run via `openclaw config patch --dry-run` | No | Yes |
| `claw-config apply <patch.json5>` | Backup → patch → restore-from-backup on failure | **Yes** | **No** |
| `claw-config report [--json]` | whoami + diagnose as markdown for pasting back to a human | No | Yes |

**Exit codes:** 0 ok / 1 runtime / 2 bad args or self cannot be resolved / 3 diagnose found a `fail`.

---

## Comparison with Adjacent Skills

| | `openclaw doctor` (built-in) | `agent-config-validator` (ClawHub) | **`claw-config`** |
|---|---|---|---|
| Scope | System-wide | Cross-agent (all of them) | Single agent (the caller) |
| Output | Human-readable only | Function returns | Plain text or JSON |
| Self-identification | N/A | Implicit | Required (`$OPENCLAW_AGENT_ID`), refuses to guess |
| Cross-agent write guard | N/A | Not enforced | Static refuse |
| Official-docs integration | None | None | `docs` + `search:` subcommands |
| Version-aware cache | N/A | N/A | Per-openclaw-version cache dir |
| Cron safety gate | N/A | N/A | `apply` hard-refused under `OPENCLAW_CRON_CONTEXT` |

---

## Install

Single-file Python 3 script + a SKILL.md frontmatter doc. No dependencies beyond stdlib + the `openclaw` and `curl` binaries (both already required for an OpenClaw setup).

```bash
git clone https://github.com/Zhili1004/claw-config.git
cd claw-config

# install into your shared OpenClaw skills directory (auto-discovered by every agent)
mkdir -p ~/.openclaw/skills/claw-config
cp SKILL.md claw-config.py ~/.openclaw/skills/claw-config/
chmod +x ~/.openclaw/skills/claw-config/claw-config.py

# symlink onto $PATH
mkdir -p ~/.local/bin
ln -s ~/.openclaw/skills/claw-config/claw-config.py \
      ~/.local/bin/claw-config

# verify
claw-config --help
```

Optional short alias:

```bash
ln -s ~/.openclaw/skills/claw-config/claw-config.py ~/.local/bin/oclm
```

---

## Quickstart Workflow

The intended order when an agent is about to change one of its own fields:

```bash
# 1. who am I — agent record + everything I own
OPENCLAW_AGENT_ID=myagent claw-config whoami

# 2. what is the field actually called? (don't guess from memory)
claw-config schema channels/telegram/accounts/myagent/commands

# 3. what does it do? (official docs, version-aware cache)
claw-config docs channels/telegram
# or grep the full corpus for a specific keyword:
claw-config docs search:nativeSkills

# 4. self-check before changing anything
OPENCLAW_AGENT_ID=myagent claw-config diagnose

# 5. compose a patch (JSON5 — comments + trailing commas allowed)
cat > /tmp/fix.json5 <<'EOF'
// re-enable native skill dispatch on telegram for myagent
{
  channels: {
    telegram: {
      accounts: {
        myagent: {
          commands: { nativeSkills: true }
        }
      }
    }
  }
}
EOF

# 6. dry-run, read the diff + validate result
OPENCLAW_AGENT_ID=myagent claw-config plan /tmp/fix.json5

# 7. live write (versioned backup + auto rollback on failure)
OPENCLAW_AGENT_ID=myagent claw-config apply /tmp/fix.json5

# 8. confirm
OPENCLAW_AGENT_ID=myagent claw-config diagnose
```

---

## Architecture Notes

- **Single-file Python script**, ~900 LOC, Python 3.9+ stdlib only.
- All writes route through `openclaw config patch` (validates internally before write). The skill adds versioned backups in `~/.openclaw/.maintenance-backups/` and `cp`-restore on failure as defense in depth.
- Docs are fetched via `curl` from `docs.openclaw.ai` (a Mintlify-powered site that natively exposes raw markdown at `<path>.md` and a full-content `llms-full.txt`). No HTML stripping. Cache TTL defaults to 24h; configurable per-call via `--max-age <hours>` or bypassable via `--refresh`.
- Cache is sharded by `openclaw --version` output. On version change, the previous version's cache dir is automatically pruned on the next `docs` call.
- 12 diagnose checks are pure-Python predicates over `openclaw config get` results — no gateway round-trip required. JSON pointers reported in diagnose output are dot/bracket notation, directly pasteable into `openclaw config get`.

---

## Compatibility

- OpenClaw `2026.5.x` and later (relies on `openclaw config patch --file --dry-run --json` flags). Should work on earlier versions where the same flags exist.
- macOS / Linux. Untested on Windows.
- Python 3.9+.

---

## Contributing

PRs welcome. Areas with known room for improvement:

- **Schema-pointer walker**: doesn't handle `oneOf` / `anyOf` branches well — currently picks the first applicable branch.
- **Cross-agent guard**: is structural, not semantic — can't detect a patch that abuses shared sections to indirectly affect another agent. Hardening welcome.
- **Binding validation**: Only Telegram-shaped bindings are validated by the `bindings_valid_peer` diagnose check. Other channel binding schemas would need their own check or generalization.

---

## Acknowledgments

- **`agent-config-validator`** by `starai-2026` (ClawHub) — adjacent skill that validates `openclaw.json` consistency across agents. Different scope (multi-agent vs. single agent) and different design (auto-fix vs. agent-composed patches), but a useful neighbor.
- **`openclaw doctor`** — the built-in system-wide health check this skill is the agent-scoped complement to.
- **OpenClaw documentation team** for shipping `<path>.md` and `llms-full.txt` raw endpoints. Made the `docs` subcommand trivially implementable.

---

## License

MIT. See `LICENSE`.