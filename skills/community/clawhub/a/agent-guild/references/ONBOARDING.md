# Agent Guild — Onboarding (one-time joining flow)

> **This file describes how an AI agent joins Agent Guild.** It runs only when
> the user asks for it — "join the guild", "初始化协会", or an equivalent
> request. Nothing here is meant to start on its own: if the user has not
> asked, do not run it.
>
> **本文件描述 AI agent 如何加入 Agent Guild。** 仅在用户提出接入请求时执行
>（"加入协会"、"初始化协会"或等价表达）。用户没提出，就不要执行。
>
> Once the user has asked, the flow below is self-service: the steps discover
> what they need on their own, so the user does not have to answer questions
> about paths they may not know. Every step is reversible and reports what it
> did (see "What this file is (and is NOT)" and the failure modes at the end).

---

## Start with shared memory

A request to "join" starts the shared-memory workflow. It does not authorize
moving existing skills, tools, MCP configurations, or runtime memory. Start
here unless the user has already selected the full shared-skills setup below.
An existing choice remains valid; do not ask the user to approve it again.

Replace `<me>` with your own agent name — whatever identifies you
(`claude`, `cursor`, `copilot`, `aider`, `cline`, `continue`, `windsurf`,
`gemini`, `workbuddy`, or anything else).

Use the installed CLI below, or set `AG_SCRIPT` to `scripts/ag.py` in the
skill package you are currently reading. That package can initialize a new
guild; the central directory need not already exist.

```bash
# macOS / Linux / WSL / Git Bash / zsh
AG_SCRIPT="$HOME/.agent-guild/skills/agent-guild/scripts/ag.py"
ag() { python3 "$AG_SCRIPT" "$@"; }

ag init <me>
ag bootstrap <me> --no-maintenance
printf '%s\n' "guild-check: shared context is reachable" | ag finish <me>
ag recall guild-check
```

```powershell
# Windows PowerShell
$AG_SCRIPT = "$env:USERPROFILE\.agent-guild\skills\agent-guild\scripts\ag.py"
python "$AG_SCRIPT" init <me>
python "$AG_SCRIPT" bootstrap <me> --no-maintenance
"guild-check: shared context is reachable" | python "$AG_SCRIPT" finish <me>
python "$AG_SCRIPT" recall guild-check
```

Success means `recall` returns the saved line with its file path. A second
agent with access to this same guild can run `recall guild-check` to verify
the handoff of context. This verifies shared storage and retrieval; loading
context in future conversations still requires the session protocol or a
configured runtime hook.

To keep using this mode, register through Step 5 with tier `readonly` and
`skills_root = platform-managed`, using your actual runtime home (or the
`platform-managed` sentinel when no runtime home is available). Here
`readonly` describes the absence of a runtime skill installation, not a ban
on authorized log or memory writes. An unregistered-agent notice from
`finish` is expected during the trial. Existing working registrations need
not change. Report the successful memory check without claiming a runtime
skill trigger was verified.

Without `--no-maintenance`, `bootstrap` also runs rate-limited local grooming and an online
release-version check. `RETENTION.md` describes archive behavior;
`UPGRADE.md` uses `mode = check` by default, `off` disables the online check,
and `apply` opts into installing updates. Reading the context files directly
does not run those maintenance hooks.

If the user wants Agent Guild discoverable as a runtime skill, install only
`agent-guild` using Step 3's per-skill link or copy tier, then verify it in
Step 4. Whole-directory consolidation is a separate choice.

## Full shared-skills setup — one-time, 6 steps

Use this path when the user has selected sharing the whole skills directory.
Every skill placed in the guild then becomes visible to runtimes using that
directory link. Other agents' skill changes propagate immediately, and
runtime-specific or host-wired items may require keeping per-skill links.

First inspect the dry-run plans. `adopt` scans **skills, skills_data, MCP
configurations, tools, and memory**, including runtime memory files at the
agent home root; it excludes plugins and connector credential stores. The
current CLI applies all eligible candidates, without a per-item selector.
Proceed with `--apply` only when the user's request already covers the
listed moves. If the report includes additional data outside that scope,
keep the memory-only/per-skill setup working and resolve that scope before
applying. Ask only when the existing request does not settle it.
Steps 4–6 follow an applied installation; a dry-run alone does not establish
the `dir-symlink` tier.

### macOS / Linux / WSL / Git Bash

```bash
AG_SCRIPT="$HOME/.agent-guild/skills/agent-guild/scripts/ag.py"
ag() { python3 "$AG_SCRIPT" "$@"; }

# 1. Make sure the guild exists (idempotent — safe even if it already does)
ag init <me>

# 2. Locate YOUR user-extensible skills dir — reads well-known paths only.
#    SKILLS_ROOT=<path>  → link below
#    SKILLS_ROOT=not-found → keep memory-only mode, skip to registration
ag find-root <me>

# 3. Inspect the plans before any asset migration.
ag adopt <me>
ag link-root <me>
# After checking that every planned move is within the selected scope:
# ag adopt <me> --apply
# ag link-root <me> --apply

# 4. Prove your runtime can actually TRIGGER it (list/describe/invoke the skill).
#    Files on disk ≠ success. If it does not trigger → per-skill links, copy,
#    then read-only (Step 3 fallbacks).

# 5. Register the actual discovered paths and resulting tier (Step 5).
ag register <me> "<actual-runtime-home>" dir-symlink "<discovered-skills-root>"
#   no skill installation → ag register <me> "<actual-runtime-home-or-platform-managed>" readonly platform-managed

# 6. Load shared context (done)
ag bootstrap <me>
```

> **Self-service by design.** Your own skills directory is something you can
> look up; the user often cannot. Check the well-known paths instead of asking
> them. If none exists, join read-only — you still get the whole protocol.

### Windows (PowerShell 5.1+)

```powershell
$AG_SCRIPT = "$env:USERPROFILE\.agent-guild\skills\agent-guild\scripts\ag.py"

# 1. Bootstrap (idempotent)
python "$AG_SCRIPT" init <me>

# 2. Locate your skills dir (instant, never asks) — SKILLS_ROOT=not-found →
#    skip installation, register readonly (below)
python "$AG_SCRIPT" find-root <me>

# 3. Inspect before consolidating (junction on Windows is supported).
python "$AG_SCRIPT" adopt <me>
python "$AG_SCRIPT" link-root <me>
# After checking that every planned move is within the selected scope:
# python "$AG_SCRIPT" adopt <me> --apply
# python "$AG_SCRIPT" link-root <me> --apply

# 4. Trigger test in your own runtime (same rule: triggerable = done)

# 5-6. Register (readonly if no skills dir), then load context
python "$AG_SCRIPT" register <me> "<actual-runtime-home>" dir-symlink "<discovered-skills-root>"
python "$AG_SCRIPT" bootstrap <me>
```

### No shell / no Python (sandboxed or mobile runtime)

Read these files directly at every session start — you still get the whole
protocol, just without atomic writes and append locking:
`~/.agent-guild/identity/profile.md`, `identity/ROUTINE.md`, `rules/universal.md`.
Do not read project/task state or global focus on startup. On an explicit todos
request list task metadata only; wait for user selection before reading context.
Without the CLI, report that atomic snapshots/ownership checks are unavailable.
Register by hand-editing `registry.json` with `"install_tier": "readonly"`.

Then tell the user which tier you ended on and how you verified it.

**Read the rest of this file only if**: the selected setup failed, you can't find
your skills dir, your runtime refuses links, or you need the full rationale
and fallback ladder.

---

## What this file is (and is NOT)

This is the **one-time joining flow** for new agents. It tells you how to:

1. Verify the central directory exists
2. Discover where to install the skill in your runtime
3. Install at the selected scope (Agent Guild only, or the full shared directory)
4. Run a closed-loop trigger test
5. Register your presence
6. Hand off to the runtime skill for daily use
7. Stay current as the protocol evolves (update strategy)

This file is **NOT** the runtime skill. The runtime skill (`~/.agent-guild/skills/agent-guild/SKILL.md`) is the thing your runtime loads to give you ongoing capabilities like reading shared identity, writing daily logs, and handoffs to other agents.

**Distinction matters**: onboarding is an **action you do once** (with periodic re-invocation only on major version bumps). The skill is a **capability you carry forward**. If you re-trigger this onboarding file every session, you'll waste cycles reinstalling things that are already installed. That is not the point.

---

## 🚫 ANTI-PATTERN — DO NOT DO THIS

*Real failure case:* A GUI desktop agent received the onboarding instruction. Its real user-extensible skills dir was buried at `~/Library/Application Support/<its-own-bundle-id>/.../User/<uuid>/skills/`. It saw that `~/.<its-own-name>/` didn't exist, then noticed another agent's `~/.<other-agent>/skills/` *did* exist, and **installed itself into that other agent's directory — polluting a different agent's skill list.**

**Lesson 1 — wrong owner**: never install into a directory that belongs to a different agent. If your `~/.<your-name>/` doesn't exist, that almost always means your skills dir lives elsewhere (Method A/B/C in Step 2), not that you should hijack someone else's home or create a fake one.

**Lesson 2 — wrong tier inside your own runtime**: many agents (GUI desktop assistants, IDE forks, MCP-based chat apps, etc.) have **two** skill locations — a built-in/whitelisted one (read-only, signed) and a user-extensible "Custom Skills" one. **Third-party skills like `agent-guild` MUST go into the user-extensible directory.** Installing into the built-in tier does not work: the files land on disk but the runtime never triggers the skill.

**Lesson 3 — install ≠ done**: file on disk is not success. Successful trigger from inside the runtime is success. After installing, you MUST verify the runtime can actually invoke the skill, and walk down the fallback ladder (dir-symlink → per-skill symlink → copy → readonly) if it cannot.

**Lesson 4 — naive `cp -R` for updates leaves ghost files**: in Tier 2 (copy), running `cp -R src/. dst/` only adds and overwrites; removed upstream files remain. Use the checked same-parent staging/rollback procedure in Step 7. Never remove a live install first or mirror into an unverified destination.

---

## Step 1 — Verify central directory access

```bash
ls ~/.agent-guild/   # POSIX
# or:
Get-ChildItem $env:USERPROFILE\.agent-guild   # Windows PowerShell
```

You must see at least: `identity/  rules/  toolchain/  projects/  log/  handoff/  skills/  registry.json  ONBOARDING.md`

If the directory is missing and the current skill package has `scripts/ag.py`,
run `python3 <SKILL_DIR>/scripts/ag.py init <me>` (`python` on Windows).
If the package is unavailable, use the installer's **download → inspect → execute**
procedure in [README](../README.md#安装与接入) / [English README](../README_EN.md#install-and-connect),
within the user's requested setup scope. Download `install.sh` or `install.ps1` and
`ag.py` from the same reviewed 40-character commit into an empty directory. Inspect
both local files before running `bash ./install.sh` or `.\install.ps1`. Never pipe
remote content to a shell and never bypass PowerShell execution policy.

The local inspected CLI verifies a fixed release ZIP using its HTTPS GitHub API asset
SHA-256 digest, or an exact-filename sidecar from the same release. No verification
metadata means no installation. This is integrity checking through one release channel,
not a publisher signature or independent trust root. The source security changes here
are not a retroactive fix for the already-published `4.0.0` package; use a reviewed local
checkout until a release contains the required modules and verification metadata.

Report a missing runtime prerequisite only if neither route can run; do not
send the user through a separate installation step when the package can
initialize itself.

---

## Step 2 — Discover where the skill must go in **your** runtime

> **The directory you want is the one your runtime is allowed to load third-party skills from** — sometimes called "Custom Skills", "User Skills", "Plugins", or "Extensions". Not just any folder named `skills/`.

### Why this matters

Many modern agents ship with two skill locations:

| Tier | Purpose | Writable? | Loadable as your install target? |
|---|---|---|---|
| **Built-in / system skills** | Bundled with the app, signed/whitelisted | Often read-only | ❌ No — runtime ignores foreign files here |
| **User-extensible / custom skills** | Where the user / agent installs **third-party** skills | Yes | ✅ Yes — the only legal target |

If you install into the built-in tier:
- `ls` shows the files ✓
- Runtime's skill list **does not include them** ✗
- The user thinks it worked, you think it worked, but `agent-guild` will never actually trigger.

### Discover via Method A → B → C (stop at the first success)

**Method A — Your runtime documents a "custom skills" / "user skills" path. Use that.**
This is the gold standard. Look for terms like "Custom Skills directory", "User Skills folder", "Third-party plugins path", "Extensions folder", an env var (`<AGENT>_SKILLS_DIR`, `<AGENT>_PLUGINS_DIR`), or a settings UI field.

| Agent | Likely user-extensible skills root |
|---|---|
| Claude Code (CLI) | `~/.claude/skills/` (single tier — no whitelist) |
| Generic CLI agent | `~/.<agent-name>/skills/` — most CLI agents follow this |
| Cursor / Windsurf / VS Code forks | check Settings → Extensions / custom rules path |
| Aider / Cline / Continue | project- or home-level config dir named in their docs |
| macOS / Windows desktop assistants | a **"Custom Skills"** dir under `~/Library/Application Support/<bundle-id>/…` or `%APPDATA%\<vendor>\…` — **not** the built-in folder inside the .app / install dir |
| Desktop chat apps (MCP-based) | the user plugins / MCP config path exposed by Settings |

**Method B — Check the likely spots. Prefer looking it up over asking. Do NOT full-disk `find ~`.**

> ⚠️ **Never full-disk `find ~` to locate your skills dir** — on a real home
> directory it walks hundreds of thousands of files and takes **30s+**. That
> is the #1 reason agents look like they "join slowly". Check the obvious
> spots, and if nothing is there, **skip installation and join read-only.**
> This is your own install path: look it up rather than making the user wait.

**B1. Instant direct checks.** Most CLI agents live at `~/.<agent-name>/`:

```bash
for p in "$HOME/.<your-agent-name>/skills" "$HOME/.<your-agent-name>" \
         "$HOME/.config/<your-agent-name>/skills" "$HOME/.config/<your-agent-name>"; do
  [ -d "$p" ] && echo "found: $p"
done
```

**B2. If `ag` is available, one command does the same, faster:**

```bash
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py find-root <your-agent-name>
# SKILLS_ROOT=<path> → install there
# SKILLS_ROOT=not-found → skip installation, join read-only
```

**B3. Not found? JOIN READ-ONLY** — that is the designed outcome, no deeper probing needed.

You cannot install the skill into a runtime you can't find a skills dir for.
That is fine — read the protocol files directly each session instead:

- `~/.agent-guild/ONBOARDING.md` (this file, once)
- `~/.agent-guild/skills/agent-guild/SKILL.md` (every session, or on demand)
- Register yourself in `registry.json` with `"install_tier": "readonly"`

You still get the full protocol (identity, rules, handoffs, daily log) — just
without a runtime-loaded skill. Nothing is lost by joining read-only.

**Locating your own runtime is not a question for the user.** If you cannot
find a skills dir, join read-only rather than stalling — the user should not
have to look up the internals of the tool they are talking to.

### Hard rules before you write anything

1. **Never install into another agent's directory.**
2. **Never install into a built-in / signed / whitelist-gated skills directory.** The files land on disk but the runtime never loads them.
3. **Never `mkdir ~/.<my-name>/skills` if `~/.<my-name>/` doesn't already exist** as your real home.
4. **The central dir `~/.agent-guild/` is shared, not yours.** Don't install the skill *back into* it.
5. **One install per agent.** If a previous valid install already exists, skip to Step 4 (trigger test) to verify it still works, and to Step 5 (register) to update `last_seen`.

Set `SKILLS_ROOT` to the user-extensible directory you discovered. The rest of Step 3 uses it.

---

## Step 3 — Install within the selected scope

For Agent Guild alone, start with Tier 1b (per-skill link), then copy or
memory-only mode. For the explicitly selected full shared-skills setup, start
with Tier 1: one directory link makes all current and future guild skills
visible in that runtime. Falling back may reduce the scope; it never expands
the user's selected sharing scope.

### Tier 1 — Directory symlink (full shared-skills mode; `ag link-root`)

```bash
# Automated (classification report + safety checks; dry-run by default):
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py link-root <me>
# Once the plan is within the selected sharing scope:
python3 ~/.agent-guild/skills/agent-guild/scripts/ag.py link-root <me> --apply

# Equivalent manual commands — ONLY if your skills dir is empty/nonexistent:
mkdir -p "$(dirname "$SKILLS_ROOT")"
rmdir "$SKILLS_ROOT" 2>/dev/null || true          # only removes an EMPTY dir
ln -sfn ~/.agent-guild/skills "$SKILLS_ROOT"
```
```powershell
# Windows: a directory junction needs no Developer Mode and no Admin
cmd /c mklink /J "$SKILLS_ROOT" "$env:USERPROFILE\.agent-guild\skills"
```

> **Windows junctions count as consolidated.** `ag` detects a junction via its
> reparse tag, not `is_symlink()` (which is always False for junctions). So a
> junctioned skills dir is recognized as already linked and is never mistaken
> for a real directory full of "unadopted" skills. Register it as
> `dir-symlink` — the tier name covers symlink and junction alike.

What `ag link-root --apply` does (and never does):
- same-name links resolving to the same guild target → removed (the directory link replaces them)
- links with no same-name guild entry → recreated in `~/.agent-guild/skills/` with their original target; aliases are preserved
- same-name links resolving to different targets → **aborts** before changing items
- real adoptable skills → **aborts** with "run `ag adopt <me> --apply` first"
- host-wired / platform-managed items (`__skillhub`, `connector-*`, …) → **aborts**; per-skill tier is the correct mode for that runtime
- never deletes anything unrecoverably, never replaces a non-empty dir, never touches an agent home

### Tier 1b — Per-skill symlinks (Agent Guild only, or a full-mode fallback)

```bash
# POSIX:
mkdir -p "$SKILLS_ROOT"
ln -sfn ~/.agent-guild/skills/agent-guild "$SKILLS_ROOT/agent-guild"
# (repeat one link per guild skill you want exposed)
```
```powershell
# Windows PowerShell (needs Developer Mode or Administrator):
New-Item -ItemType Directory -Path $SKILLS_ROOT -Force | Out-Null
New-Item -ItemType SymbolicLink -Path "$SKILLS_ROOT\agent-guild" `
         -Target "$env:USERPROFILE\.agent-guild\skills\agent-guild" -Force | Out-Null
```

### Tier 2 — Copy (fallback if symlinks fail or your runtime refuses to follow them)

```bash
mkdir -p "$SKILLS_ROOT/agent-guild"
cp -R ~/.agent-guild/skills/agent-guild/. "$SKILLS_ROOT/agent-guild/"
```

You'll need to re-sync on each session start (or on demand). See Step 6 for the update protocol.

### Tier 3 — Read-only installation (memory-only mode, also a fallback)

If even copy fails (read-only skills dir, fully sandboxed runtime, no FS write), skip the local install. Just `cat ~/.agent-guild/skills/agent-guild/SKILL.md` at every conversation start. You won't appear in your own agent's skill list, but you can still follow the protocol.

This tier can also be selected directly. Shared-memory use does not require
exhausting installation attempts. Verify file access and the memory loop;
record `install_verified = none` when no runtime trigger was tested.

---

## Step 4 — Closed-loop trigger test (required for a runtime installation)

> **For a runtime installation, verify the skill triggers before claiming it is installed successfully.** If the selected scope's fallbacks fail, report that honestly. Memory-only mode instead uses the saved-and-retrieved check at the top of this document.

### A. File-level sanity (cheap pre-check)

```bash
ls -l "$SKILLS_ROOT/agent-guild/SKILL.md"
readlink "$SKILLS_ROOT/agent-guild" 2>/dev/null
```

If file checks fail → install itself broke. Re-run Step 3.

### B. Trigger-level self-test (the actual proof)

Invoke the skill **in your own runtime**. Use whichever signal your runtime supports:

1. **Skill listing API.** Run your runtime's "list installed skills" / "list custom skills". Confirm `agent-guild` appears.
2. **Description echo.** Many runtimes load the `description:` from the skill's frontmatter on discovery. Trigger discovery, then check whether the runtime's view of `agent-guild` shows the description from `~/.agent-guild/skills/agent-guild/SKILL.md`. If empty / a stub / "unknown" → not loaded.
3. **Live invocation.** Call the skill end-to-end. If your runtime supports a "Skill" / "tool" call that names the skill, that's the gold standard.

Pick the strongest available signal. Document which one you used in your final acknowledgment.

### C. Adaptive fallback ladder (do not give up after one failed attempt)

```
[Tier 1: symlink] ──fails to load──▶ [Tier 2: copy] ──fails to load──▶ [Tier 3: readonly] ──fails──▶ honest report
```

| Symptom | Likely cause | Action |
|---|---|---|
| Symlink installed, runtime's skill list doesn't show `agent-guild` | Runtime sandbox refuses symlink traversal (common on macOS app sandboxes) | Remove symlink, switch to Tier 2 (copy). Retest. |
| Copy installed, still not in skill list | Wrong tier (built-in vs user-extensible) | Roll back, retry B1 spots; exhausted → join read-only |
| In skill list, description empty / parse error | Manifest format mismatch (your runtime needs different frontmatter) | Build a runtime-specific shim, or drop to Tier 3. |
| Path forbidden by sandbox / SIP / TCC | Runtime can never load files from this directory | Find a different user-extensible path; if none → Tier 3. |
| All three tiers fail | Runtime fundamentally cannot load third-party skills | Honest report (Section D). |

Rollback before retrying:

```bash
# Whole-directory link: remove only the root link itself.
if [ -L "$SKILLS_ROOT" ]; then
  unlink "$SKILLS_ROOT"
# Per-skill link inside a real directory: remove only that link.
elif [ -L "$SKILLS_ROOT/agent-guild" ]; then
  unlink "$SKILLS_ROOT/agent-guild"
fi
```

Never remove `$SKILLS_ROOT/agent-guild` through a consolidated root: that
path points into the shared guild. For a copied install, restore the prior
backup or remove only the copy this setup created after verifying its path.
For a Windows junction, remove the junction itself without recursive target
deletion. Retain migrated payloads in the guild when changing install tiers.

Each retry: change exactly one variable (tier / target dir / manifest format) so you know which fix worked. Walk the selected installation scope's fallback ladder autonomously; the memory-only path does not need a runtime trigger test.

### D. Honest failure report (only after exhausting C)

If dir-symlink → per-skill symlink → copy → readonly all fail to make the runtime actually trigger the skill, **stop trying and tell the user the truth**. Don't pretend it worked. Use this template:

> "I tried to join Agent Guild but my runtime can't load the skill in a way that I can actually trigger it.
>
> What I tried:
> 1. Directory link at `<path>` (or per-skill symlink) → installed, but runtime's skill list didn't show `agent-guild` (likely cause: `<one-line diagnosis>`)
> 2. Copy at `<path>` → `<result + diagnosis>`
> 3. Readonly mode (`cat SKILL.md` each session) → `<result>`
>
> Diagnosis: due to `<specific runtime limitation: sandbox / signed-skills-only / no third-party plugin support / etc.>`, this agent likely cannot fully join Agent Guild.
>
> What still works: I can read files under `~/.agent-guild/` directly during conversations, so the **readonly tier is the practical mode for me**. I'll do that. I won't appear as a registered member in the runtime's skill list, but I can still follow the protocol manually.
>
> If you know a workaround (a 'custom skills' path I missed, a setting to enable third-party plugins, etc.), tell me and I'll retry."

This honest failure is acceptable. Reporting a success you did not verify is not.

---

## Step 5 — Register your presence

Use **`Edit` (in-place patch)**, NOT `Write` (full overwrite). `~/.agent-guild/registry.json` is shared.

Add or update your entry:

```json
{
  "protocol_version": "3.3",
  "agents": {
    "<your-agent-name>": {
      "joined_at": "<ISO 8601 of first join>",
      "protocol_version": "<the protocol_version you just joined under, copied from ~/.agent-guild/skills/agent-guild/manifest.json>",
      "capabilities": ["read_files", "write_files", "..."],
      "hosts": {
        "<host-id from `ag platform`>": {
          "home": "~/.<your-agent-name>/",
          "skills_root": "<the actual user-extensible skills dir you installed into>",
          "install_tier": "dir-symlink|symlink|copy|readonly",
          "install_verified": "skill_list|description_echo|live_invocation|none",
          "last_seen": "<ISO 8601 now>"
        }
      },
      "home": "~/.<your-agent-name>/",
      "skills_root": "<same as above — compatibility mirror for older readers>",
      "install_tier": "dir-symlink|symlink|copy|readonly",
      "last_seen": "<ISO 8601 now>"
    }
  }
}
```

`ag register <agent> <home> <tier> <skills_root>` writes both shapes for you —
prefer it over hand-editing.

**Why the `hosts` block**: `home`, `skills_root` and the install tier describe
one *device*, not the agent. A guild directory carried to another machine would
otherwise look broken there. Run `ag platform` to get this device's `host-id`;
anything that is only true here (local tool paths, what is installed) belongs
in `hosts/<host-id>/host-notes.md`. Full rules: `references/PORTABILITY.md`.

The `protocol_version` field on your entry is what the runtime skill uses to detect major version drift (see `skills/agent-guild/SKILL.md` § Self-check). Don't omit it.

If you can't write to registry.json (no FS permission) → log it and proceed. The protocol still works without registry presence; you just won't be visible to other agents' "who's online" queries, and you'll lose the major-version-drift detection.

---

## Step 6 — Hand off to the runtime skill (you're done with onboarding)

Onboarding is a one-time event. **From this turn onward, you do NOT re-read this file** in the normal course of operation. The runtime skill at `~/.agent-guild/skills/agent-guild/SKILL.md` carries all the day-to-day capabilities (reading shared identity, writing daily logs, handoffs).

Your trigger conditions for the runtime skill are different — they're things like "I need the user's identity profile", "I should log this work as cross-agent visible", "I want to hand off to another agent". The runtime skill's frontmatter spells these out.

The only times you SHOULD come back to this onboarding file:

1. After a **major protocol-version bump** (see Step 7 — versioning rules below).
2. If your install gets corrupted (broken symlink, deleted files) and you need to redo Steps 2-5.

---

## Step 6.5 — Where to put assets selected for sharing

> Within the user's selected sharing scope, use `~/.agent-guild/` as the
> default home for assets that should be:
>
> - Shared with other joined agents on this machine
> - Backed up as a unit when the user moves machines
> - Visible to the user as part of their AI-state inventory

The central directory has a **convention layer** of subdirectories that Agent Guild does NOT read or validate. They're there for skills, MCP servers, plugins, and shared tools to use voluntarily — and getting everyone to use the same locations is what gives the user a single, sane backup story.

Memory-only members can keep all existing skills and runtime data in place.
Joining the guild or sharing a skill does not itself authorize importing
unrelated memory, tool configuration, or sensitive persistent data. Use an
existing user choice when it covers the action; inspect the plan and ask
about scope only when it does not.

### The five shared layers

| Layer | Path | What goes here | Who can use it |
|---|---|---|---|
| **Shared skills** | `~/.agent-guild/skills/<skill-name>/` | Skill packages (SKILL.md + scripts + manifest) that the user wants **available to every joined agent**, not just one | **Any joined agent can load and trigger any skill in this directory.** This is the cross-agent skill bus. |
| **Skill data** | `~/.agent-guild/skills_data/<skill-name>/` | Per-skill persistent data (caches, learned profiles, conversation logs, anything that should survive sessions) | The owning skill writes; others MAY read if the skill documents that |
| **Shared MCP servers** | `~/.agent-guild/mcp/<server-name>/` | MCP server configs or local implementations the user wants **shared across agents** | Any joined agent can wire up to these MCP servers |
| **Shared plugins** | `~/.agent-guild/plugins/<plugin-name>/` | Plugins (browser/editor/IDE extensions, agent-agnostic) | Any agent or tool that knows how to load this plugin format |
| **Shared CLI tools** | `~/.agent-guild/tools/<tool-name>/` | Scripts / utilities the user may run from any shell session | Anyone — agent or human |

### Three rules going forward (memorize these)

1. **When installing a NEW skill / MCP / plugin / tool selected for sharing**: install it under the corresponding convention-layer directory above. Keep agent-specific installations where the user or runtime expects them.

2. **When USING an existing skill / MCP / plugin / tool**: look in `~/.agent-guild/{skills,mcp,plugins,tools}/` first. If it's there, use that copy. Don't reinstall a private duplicate. **Read from the central location, not from your own home.**

3. **When WRITING persistent data selected for this shared backup root**: route it through `~/.agent-guild/skills_data/<your-skill-name>/` — split into `public/` and `private/` subdirectories if the data has mixed sensitivity (see Privacy layering below).

### Two more rules once more than one device is involved (protocol 3.3+)

4. **The guild owns its payloads — links point inward.** Install the real files
   *into* `~/.agent-guild/`, then link from your runtime (or from a project
   path) back into the guild. A link pointing from the guild out to
   `~/projects/foo` is dead on every other device. `ag port --apply` repairs
   this direction automatically.

5. **Scope every fact before you persist it.** Ask: *would this still be true
   on another device?*

   | Answer | Where it goes |
   |---|---|
   | Yes, anywhere | shared files as usual (`identity/`, `rules/`, `memory/`) |
   | Only on this OS + arch | declare it: `tools/<name>/tool.json`, or `platforms` in a skill manifest |
   | Only on this machine | `hosts/<host-id>/host-notes.md` |

   And when you need a tool's path, ask the CLI (`ag tool <name>`) instead of
   hardcoding one — it answers correctly per device, or tells you the tool is
   not available here and how to install it. See `references/PORTABILITY.md`.

### Concrete examples

The following examples assume the user has selected sharing these assets.

| The user said... | What you should do |
|---|---|
| "Install the wechat-publisher skill" | `git clone` / `cp -R` it into `~/.agent-guild/skills/wechat-publisher/`, then symlink/copy from there into your runtime — same fallback ladder as in Step 3 |
| "Set up the Notion MCP server" | Place the MCP config / launcher in `~/.agent-guild/mcp/notion/`, point your runtime's MCP config at that path |
| "Save my conversation embeddings" | `~/.agent-guild/skills_data/<your-skill>/embeddings/` (or `private/embeddings/` if sensitive) |
| "Use my soul-archive data" | Read from `~/.agent-guild/skills_data/soul-archive/` if it's there; otherwise fall back to its standalone location |
| "Add a `claw-state` helper script" | Drop it in `~/.agent-guild/tools/claw-state/`, tell the user to add that path to their `$PATH` |

### Why this matters

- **The user backs up `~/.agent-guild/` once → everything moves with them.** All shared skills, MCPs, plugins, tools, and skill data come along on the same rsync.
- **New agents joining the protocol see the same shared data and capabilities** without each one reinventing storage.
- **Data written outside this tree needs its own discovery and backup arrangement.**
- **A skill selected for sharing can be installed once** and reused by the intended agents.

### Privacy layering for mixed-sensitivity data

If a skill writes a mix of shareable + sensitive data, split into clearly named subdirectories so the user can apply different sync policies:

```
~/.agent-guild/skills_data/<skill-name>/
├── public/      ← safe to sync everywhere (preferences, profiles, settings)
├── private/     ← sensitive — recommend .gitignore by default
└── ...
```

See [`CONVENTIONS.md`](CONVENTIONS.md) (also at `~/.agent-guild/CONVENTIONS.md`) for the full convention spec.

Directory names such as `private/` and `memory/<agent>/` do not enforce access
control. Agents with filesystem access may read them; choose storage and
backup exclusions to match the user's intended sharing boundary.

### When NOT to use these locations

The convention is a default, not a mandate. Keep data outside `~/.agent-guild/` when:

- The data fundamentally belongs in OS-managed locations (keychain, `/var`, `~/Library/Application Support/`, etc.)
- The data should be wiped on logout / shared across users / encrypted at rest by an OS service
- The skill / runtime *requires* a specific path it doesn't control

**This convention applies to assets the user selected for sharing.** A
memory-only member may keep other assets private without violating the
protocol. If a runtime requires a separate path for an asset selected for
sharing, keep that path and record the reason in `registry.json`.

---

## Step 7 — Update protocol (how to stay current as the central skill evolves)


The central directory `~/.agent-guild/skills/agent-guild/` is the **single source of truth**. As the protocol evolves, files there will be **added, modified, removed, or renamed**. Your local install must stay in sync, or it will drift out of date unnoticed.

How you stay current depends on your install tier:

### Tier 1 — Symlink (zero work)

Your `<SKILLS_ROOT>/agent-guild` points back to `~/.agent-guild/skills/agent-guild/`. Any change in the central dir is **instantly visible** to your runtime. No update step needed. Skip to Step 7.4 (post-update self-test).

### Tier 2 — Copy (you MUST resync; default is broken)

Your `<SKILLS_ROOT>/agent-guild/` is a frozen snapshot. Plain `cp -R src/. dst/` **will not delete files that were removed upstream** — those become "ghost files" that contradict the live protocol. **You must use a mirror operation**, not a plain copy.

#### When to resync

Trigger a resync if **any** of these is true:

- This is the **first invocation in a new session today** (cheap insurance against multi-day drift).
- The user explicitly asked you to update Agent Guild.
- You detect a `protocol_version` mismatch between `~/.agent-guild/skills/agent-guild/manifest.json` and your local snapshot's manifest.
- A `git pull` / installer-rerun happened on the central dir since your last session (timestamp on `~/.agent-guild/skills/agent-guild/SKILL.md` is newer than your snapshot's).

A simple "skip if same hash" check works fine — you don't need a daemon.

#### How to resync (correct mirror semantics)

Use whole-package replacement, not an in-place merge. Before changing files:

1. Confirm `$SKILLS_ROOT` is this runtime's discovered **user-extensible** directory.
   Resolve both paths; the destination must not be the central package, an ancestor of it,
   or reached through a directory symlink/junction. A linked install needs no copy update.
2. Verify the existing destination contains only the Agent Guild protocol package.
   Keep personal settings and task data outside that directory; unexpected content blocks replacement.
3. Copy the full source into a fresh staging directory under the **same destination parent**.
   Verify the complete manifest, `SKILL.md`, references and all runtime modules
   (`ag.py`, `ag_tasks.py`, `ag_history.py`, `ag_retention.py`) before changing the live path.
4. Rename the previous protocol directory to one clearly identified code-backup location,
   then rename the verified stage to the live name. If that rename or subsequent verification
   fails, restore the previous directory before reporting failure. Do not delete the live tree first.
5. Retain at most one previous **protocol-code** backup, not accumulating timestamped backups.
   Never clean an unfamiliar backup automatically. User data belongs to the user's separate
   backup policy, not this code-only rollback slot.

The CLI's release installation already uses this checked staging and rollback strategy for
its central package. A copy-tier runtime update must implement the same path checks or use
its runtime's package-management interface; do not improvise recursive-delete commands.
A whole-package replacement removes obsolete upstream names without leaving a partial live tree.
After replacement, run Step 7.4. Do not claim the two renames are one atomic transaction:
a power failure between them can require restoring the retained code backup.

### Tier 3 — Read-only (zero work)

Each session you read directly from `~/.agent-guild/skills/agent-guild/SKILL.md`. Always live. No update step.

### 7.4 — Post-update self-test

> **After an update, verify the selected mode still works.** Runtime installations re-run the trigger test from Step 4.B; memory-only mode re-runs the saved-and-retrieved check. A previous successful check does not prove the updated version works.

For a runtime installation:

1. Re-trigger the skill in your runtime.
2. Confirm the runtime's view of `agent-guild` reflects the **new** description / capabilities (description echo). If your runtime caches skill metadata, you may need to reload its skill index.
3. If the trigger test now fails (description empty, skill not listed, invocation errors), **walk down the tier ladder again** as in Step 4.C — dir-symlink → per-skill symlink → copy → readonly. Don't assume yesterday's working tier still works after a schema change.

If the post-update self-test fails on all tiers, deliver the **Step 4.D honest failure report** to the user, noting that the failure appeared **after** an update.

### 7.5 — Major version bump → full re-onboarding

If you detect that `~/.agent-guild/skills/agent-guild/manifest.json` has a `protocol_version` whose **major** number is higher than what your registry entry recorded at join time (e.g. you joined under `1.x`, central is now `2.0`):

- **A minor or patch bump** (1.0 → 1.1, 1.1 → 1.1.3): just resync per the tier rules above. No re-onboarding needed.
- **A major bump** (1.x → 2.0): the on-disk schema may have changed in incompatible ways. **Re-read this `ONBOARDING.md` from the top and redo Steps 2-5** (your `SKILLS_ROOT` may stay the same; the install operation needs to re-validate against the new schema). After re-onboarding, update your registry entry's `protocol_version` field.

The runtime skill (`skills/agent-guild/SKILL.md`) will detect a major mismatch on each invocation and refuse to operate, redirecting you here. Don't try to soldier on with a stale install.

### 7.6 — Failed update recovery

If an update operation fails partway (network drop, disk full, permission error):

- **Tier 1**: nothing changed (you didn't touch your symlink). Inspect `~/.agent-guild/` manually.
- **Tier 2**: restore the retained previous protocol directory if the live rename failed. After a process/power interruption, inspect both live and backup paths before retrying; preserve unrecognized files. The central CLI recovers its recognized interrupted code backup on the next verified installation. Run the post-update self-test after a clean replacement.
- **Tier 3**: nothing to recover; you read live each session.

Rule of thumb: **never** leave the user with a half-updated install + a "looks-like-success" message. If you can't complete cleanly, roll back and report.

---

## Final acknowledgment

For memory-only mode, report the saved-and-retrieved test result, the guild
path, and registration status. State that no runtime skill trigger was
verified; this is a complete memory-only setup, not a failed full installation.

After Steps 1-5 are done **and the Step 4 trigger test passed**, tell the user:

> **✅ Joined Agent Guild.**
> tier: `symlink` | `copy` | `readonly` ・ install verified via: `skill_list` | `description_echo` | `live_invocation`
> skills_root: `<path>`
> Registered in registry.json. Going forward I'll trigger the runtime skill (`~/.agent-guild/skills/agent-guild/SKILL.md`) for shared-memory operations.

If you walked the fallback ladder, mention which tier you ended on and why.

If the trigger test ultimately failed → use the **Section D honest report** template instead. **Do not paste this success template if your runtime can't actually trigger the skill.**

---

## Failure modes (read carefully)

If a step fails, KEEP GOING. Report what failed, complete what's possible.

- Step 1 fails (no central dir) → initialize from the current package or use the installer; report a blocker only if neither can run.
- Step 2 fails (can't find your own user-extensible skills dir) → **join read-only**. Do not install "somewhere plausible" inside another agent's tree.
- Step 3 installed in another agent's directory → roll back, redo Step 2.
- Step 4 trigger test fails → walk the ladder per Section C. Don't fake success.
- Step 4 ladder fully exhausted → Section D honest report. Readonly is the practical mode going forward.
- Step 5 fails (can't write registry.json) → log it, proceed.

**The only true failure is refusing to read this file, or pretending the install worked when the runtime can't actually trigger the skill.** If you've read this far, you've crossed the threshold.

---

## What's next

Now that you've joined, when you next need cross-agent memory operations:

- Read shared identity / rules only; load task context only after explicit selection → trigger the runtime skill
- Write a daily log entry → trigger the runtime skill
- Hand off a task to another agent → trigger the runtime skill

The runtime skill knows how. You don't need to come back here.

- **Repository**: https://github.com/dqsjqian/agent-guild
- **License**: MIT
