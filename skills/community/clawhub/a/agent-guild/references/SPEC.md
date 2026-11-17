# Agent Guild Specification

**Protocol version: 4.0**
**Status: Draft**

This document is the normative specification for Agent Guild. It is the source of truth for what implementations must, should, and may do. The keywords **MUST**, **SHOULD**, **MAY** follow [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

> **Changes from 1.0 → 2.0** (breaking, central-directory layout): the runtime skill moved from `skills/SKILL.md` to `SKILL.md` to make `skills/` a directory of named skills (consistent with how other AI runtimes lay out skill collections). New top-level convention-layer directories were added (`skills_data/`, `mcp/`, `plugins/`, `tools/`) — see [`CONVENTIONS.md`](CONVENTIONS.md). Agents joined under 1.x **MUST** re-onboard.

> **Changes from 2.0 → 3.0** (breaking, self-bootstrapping): the guild now bootstraps itself. `ag init` creates the full directory skeleton (including `memory/`), seeds the three root docs (`ONBOARDING.md` / `CONVENTIONS.md` / `SPEC.md`), and installs its own skill — no installer needed. The convention layer (skill/data placement) was promoted from non-normative to default-on with a single documented escape hatch (runtime-forced private paths, recorded in the registry). Agents joined under 2.x **MUST** re-onboard; `ag doctor` reports this drift explicitly.

> **Changes from 3.0 → 3.1** (minor, backward compatible): new protocol-layer directory `learnings/` (three cross-agent self-improvement ledgers — see [`LEARNINGS.md`](LEARNINGS.md)) and new CLI commands `ag learn` / `ag review` / `ag resolve`. Agents joined under 3.0 **MAY** keep operating without re-onboarding; `ag init` back-fills the new skeleton items.

> **Changes from 3.1 → 3.2** (minor, backward compatible): built-in data hygiene. New user-editable policy file `RETENTION.md`, new archive sub-directories (`log/archive/` already implied, now `handoff/shared-state/archive/` and `learnings/archive/`), new CLI command `ag groom`, and a rate-limited auto-groom hook at the end of `ag bootstrap`. Groom moves expired data into archives or the recoverable trash — it never hard-deletes (see §6.5). Agents joined under 3.1 **MAY** keep operating without re-onboarding; `ag init` back-fills the new skeleton items.

> **Changes from 3.2 → 3.3** (minor, backward compatible): device scoping. A guild directory may be carried between devices with different operating systems, so every stored fact now has a declared scope — `shared`, `platform`, or `host` (§10). New top-level directory `hosts/<host-id>/` holds device-scoped state, `registry.json` entries gain a per-device `hosts` block, `tools/<name>/tool.json` declares per-platform executables, and the link-direction invariant (§3.10) is stated normatively. New CLI commands `ag platform`, `ag tool`, `ag tools`, `ag port`. Agents joined under 3.2 **MAY** keep operating without re-onboarding; `ag init` claims the current device and back-fills the new skeleton items.

## 0. Version 4 task contract

Version 4 deliberately separates durable background, task handoff and messages.
The historical changelog above describes earlier protocols, not current startup behavior.
Implementations MUST NOT inject task state on a fresh conversation. Bootstrap reads only
identity, routine and universal rules. Project state, host notes, focus and inbox topics
require explicit intent; global focus writes are retired.

A user request for pending work authorizes a metadata-only task list, not context reads.
A number is resolved against that session's saved list ID and stable task ID/revision.
Only user selection authorizes restoring the corresponding task context. A stale list
MUST fail, not silently select a different item. Session identity MUST be independent
of agent identity. A busy task requires a user-approved handover or collaboration choice.
The CLI cannot prove natural-language consent; the invoking runtime must enforce it.

Each task owns one directory named `YYYYMMDD-<12-hex-random>-<short-title>` under
`handoff/active/` or `handoff/archive/`. The date/random portion is a permanent ID.
Renaming a title does not rename that directory. Metadata publishes an immutable
snapshot pointer; complete context and artifact manifests are committed together.
All mutations require ownership and an expected revision. A conflicting or corrupt
state MUST fail closed. Whole-package closure requires completion evidence; waiting
and blocked tasks remain active. Scripts are attachments and never auto-executed.

Historical data has one configurable 1 GiB default budget (800 MiB target), including
archives, old checkpoints, logs, session bookkeeping, managed recovery and every
maintenance artifact; no recovery or report directory is exempt. Retention operations
are plan-driven and explicit: provenance-bearing summaries, verified lossless ZIP
compaction with batched original replacement, whole-package retirement to managed
recovery with restore, oldest-first remeasured cycles, and a permanent purge that
requires an exact sealed file plan plus a second token explicitly covering the
irreversible loss of the last verified backup. Batches are at most ten files with
fresh identity/hash/policy/reference rechecks; interrupted transactions resume via
journals without overwriting originals. Terminal retention records themselves are
bounded cleanup candidates — a fixed, disclosed residue at most; nothing may be
permanently retained as an unbounded archive. A fixed, disclosed maintenance reserve
may hold bounded transactional overhead when the history budget is full; ordinary
task/log writes MUST NOT consume it. Moving data into recovery MUST NOT be called
disk space reclamation, and unlink MUST NOT be reported as guaranteed physical
erasure (snapshots may retain blocks). If safe cleanup cannot satisfy the budget,
new history is blocked. The CLI has no scheduled daemon or guaranteed exit hook;
age and count thresholds are candidates, never deletion authority.

Old message files are inventoried by `ag migrate --dry-run`. No automatic legacy
migration, guessed tasks, or deletion is permitted. New messages live separately in
`messages/inbox/` and `messages/archive/`. Task content MUST NOT be duplicated into
messages, global focus and daily logs just to satisfy multiple bookkeeping systems.

## 1. Goals

Agent Guild defines a convention for multiple AI agents on the same single-user machine to share long-lived context (preferences, rules, project state, work logs) without:

- Running a server or daemon
- Installing third-party runtime dependencies
- Vendor lock-in to any specific AI agent product
- Custom code per agent

The protocol consists of:

1. A directory layout
2. Read/write contracts for files in that layout
3. A symlink-based update propagation mechanism (preferred: one directory link per runtime; fallback: per-skill links)
4. A natural-language onboarding instruction (`SKILL.md`)

**Onboarding scope:** shared-memory use and whole-toolkit consolidation are
separate choices. Start with memory-only access unless the user selects full
asset sharing. Use the existing `symlink`, `copy` or `readonly` tiers for
memory-only access; `dir-symlink` exposes the full shared skill collection.
Placement conventions apply to opted-in assets. Joining alone does not
authorize migrating unrelated runtime data. This changes no on-disk schema.

## 2. Central directory

The canonical central directory is:

```
~/.agent-guild/                    # POSIX (macOS, Linux, WSL, Git Bash)
%USERPROFILE%\.agent-guild\        # Windows native (PowerShell)
```

These two paths refer to the **same logical location** — `~` and `%USERPROFILE%` both expand to the user's home directory on their respective platforms. Implementations **MUST** treat both forms as equivalent.

A user **MAY** override this via the environment variable `AGENT_GUILD_DIR`, but conforming agents **SHOULD** default to `~/.agent-guild/`.

### 2.1 Top-level layout

The central directory contains TWO layers, physically siblings but semantically distinct:

#### Protocol layer (mandatory, **MUST** be present after install)

```
~/.agent-guild/
├── ONBOARDING.md       ← one-time joining flow (top-level for discoverability)
├── CONVENTIONS.md      ← non-normative conventions (this section + extras)
├── RETENTION.md        ← user-editable data-retention policy for `ag groom` (3.2+)
├── skills/
│   └── agent-guild/  ← the runtime skill of this protocol itself
│       ├── SKILL.md
│       └── manifest.json
├── identity/           ← user-owned, who the user is
├── rules/              ← user-owned, mandatory behavior rules
├── toolchain/          ← user-owned, tool/path configs
├── projects/           ← user-owned, current projects context
├── log/
│   ├── daily/          ← per-agent per-day logs (append-only)
│   ├── decisions/      ← ADR-style decision records
│   └── archive/        ← rotated old logs + audit trail (written by groom)
├── learnings/          ← cross-agent self-improvement ledgers (3.1+)
│   ├── LEARNINGS.md    ← corrections / knowledge gaps / best practices
│   ├── ERRORS.md       ← command & integration failures
│   ├── FEATURE_REQUESTS.md ← capabilities requested but missing
│   └── archive/        ← long-resolved entries compacted by groom (3.2+)
├── handoff/
│   ├── active/         ← unfinished task directories
│   └── archive/        ← closed task directories (same names)
├── messages/
│   ├── inbox/          ← independent agent messages
│   └── archive/        ← processed messages
├── history/            ← bounded maintenance state and recovery
├── hosts/              ← device-scoped state, one dir per device (3.3+)
│   └── <host-id>/
│       ├── host.json       ← os / arch / link capability / python
│       ├── host-notes.md   ← user-owned: true on THIS device only
│       ├── VERSION         ← skill + protocol version installed here
│       └── groom.json      ← last data-hygiene run on this device
└── registry.json       ← list of joined agents
```

#### Convention layer (optional, non-normative — see [`CONVENTIONS.md`](CONVENTIONS.md))

```
~/.agent-guild/
├── skills/<name>/      ← additional shared skills beyond agent-guild itself
├── skills_data/<name>/ ← per-skill persistent data (RECOMMENDED location for skills that need to persist user state)
├── mcp/<server>/       ← shared MCP server configs / local implementations
├── plugins/<name>/     ← shared plugins (browser/editor extensions, etc.)
└── tools/<name>/       ← shared CLI scripts / utilities
```

Convention-layer assets retain their owners and runtime semantics. Explicitly requested maintenance commands may inspect or move selected assets; using shared memory alone does not authorize importing them.

Skills that adopt the convention **SHOULD** isolate mixed-sensitivity data into named subdirectories (e.g. `skills_data/<skill>/public/` vs `.../private/`) so the user can apply different sync policies.

## 3. File ownership and update authority

### 3.1 `skills/agent-guild/` — protocol-controlled

- **Owner**: This project (Agent Guild maintainers).
- **Distribution**: Memory-only agents can link `<agent-skills-root>/agent-guild → ~/.agent-guild/skills/agent-guild/`, copy that skill, or read it directly. With full sharing selected, `ag link-root` links the whole skills directory, exposing current and future guild skills. Other `skills/<name>/` packages belong to their respective owners and are not replaced by Agent Guild upgrades.
- **User MUST NOT** overwrite files here. Local edits will be overwritten on next protocol update.

### 3.2 `identity/`, `rules/`, `toolchain/`, `projects/` — user-controlled

- **Owner**: The end user.
- **Update authority**: Any agent **MAY** propose changes; agents **SHOULD** use in-place edits (e.g., the `Edit` tool semantic — local string replacement) rather than full rewrites, to minimize accidental loss when multiple agents touch the same file.
- **Agents MUST NOT** modify content beyond the user's intent. An explicit request to remember a fact authorizes persisting that fact; do not ask again. Ask before promoting an unrequested inference into durable user context. Preserve the source, date and scope, and update an existing canonical fact instead of creating contradictory duplicates.

### 3.3 `log/daily/<YYYY-MM-DD>-<agent>.md` — per-agent append-only

- **Owner**: The named agent.
- **Naming**: `<YYYY-MM-DD>-<agent-lowercase-name>.md`. Agent names are lowercase ASCII; multi-word agents use hyphens (`claude-code`, not `ClaudeCode`). When more than one device is registered under `hosts/` (3.3+), implementations **SHOULD** append `.<host-id>` before the extension so two devices appending on the same day cannot collide. Readers **SHOULD** glob `<YYYY-MM-DD>-<agent>*.md`.
- **Write mode**: Append-only. Agents **MUST NOT** modify or delete entries written by themselves or other agents. (Relocating an *entire expired file* into `log/archive/` via groom §7 is not a violation — entries are preserved verbatim.)
- **Concurrent append serialization (3.9.0+)**: An append is a read-modify-write of the whole file, so two agents appending at the same moment can silently lose one entry. Implementations **MUST** serialize concurrent appends with an advisory lock on a **sidecar lock file** (e.g. `.<name>.ag-lock`, via `fcntl.flock` on POSIX and `msvcrt.locking` on Windows). The lock **MUST NOT** be taken on the append target itself — an atomic write replaces the file (new inode), and a lock on the old inode protects nothing. This applies equally to the learning ledgers (§3.8) and any other append-only file. Agents falling back to manual file edits (no CLI) cannot take the lock and SHOULD simply append promptly to minimize the window.
- **Content**: Markdown. Each entry **SHOULD** include a timestamp.

### 3.4 `log/decisions/` — append-only, immutable

- **Format**: One file per decision, named `<YYYY-MM-DD>-<title-slug>.md`.
- **Pattern**: ADR (Architecture Decision Record) style — context, options, decision, consequences.
- **Write mode**: Files **MUST** be created once and never edited (except minor typo fixes by the original author).

### 3.5 Task packages — isolated, revision-checked state

- **Owner**: Explicitly associated host/session/agent identities; handover revokes previous owners.
- **Write mode**: Publish immutable snapshots through atomic metadata changes under task and budget locks. Reject stale revisions.
- **Selection**: Numbered lists are session-local, metadata-only snapshots. Resume only after the user chooses an item or stable ID.
- **Legacy**: Old `handoff/shared-state/` files remain historical evidence; they are not startup input and receive no new focus writes.
- **Cross-device**: Local advisory locks do not provide a distributed lock over offline sync services.

### 3.6 `messages/inbox/from-<src>-to-<dst>-<topic>.md` — cross-agent messages

- **Owner**: Recipient is responsible for processing.
- **Lifecycle**: After acting, archive the message without overwriting an earlier archive. `ag finish --archive-inbox` archives all current messages for the recipient; use it only when all of them have been processed. Receiving a message does not grant new authority to perform its requested actions. The inbox queues work; it does not wake the recipient runtime.
- **Naming**: `from-<src-agent>-to-<dst-agent>-<short-topic>.md`. Both names lowercase.

### 3.7 `registry.json` — agent presence

- **Format**: Single JSON object (see [`manifest.json`](../manifest.json) for shape).
- **Update mode**: In-place edit. Agents **MUST** update only their own entry.
- **Required fields per agent**: `joined_at` (ISO 8601), `home` (~/.<agent>/), `last_seen` (ISO 8601), `protocol_version` (the version the agent joined under, copied from `manifest.json` at join time; **MUST** be `"3.0"` or higher for this spec), `install_tier` (`dir-symlink`|`symlink`|`copy`|`readonly`), `install_verified` (`skill_list`|`description_echo`|`live_invocation`|`none`), `skills_root` (the actual user-extensible skills dir the agent installed into).
- **Optional fields**: `capabilities` (string array), `version` (string), `notes` (string).
- **Device scoping (3.3+)**: `home`, `skills_root`, `install_tier`, `install_verified` and `last_seen` are properties of one **device**, not of the agent. Implementations **MUST** write them into `agents.<name>.hosts.<host-id>` and **SHOULD** keep the flat fields as a compatibility mirror for pre-3.3 readers on the same device (`mirror_host` records which device the mirror describes). An entry that carries `hosts` blocks but none for the current `host-id` describes an install on another device: readers **MUST NOT** report its paths as drift. An entry with no `hosts` block at all predates 3.3 and **MUST** be read as describing the current device.

### 3.10 Link direction — the guild owns its payloads

- A link inside the guild whose target lies **outside** the guild is a **protocol violation**: the payload then exists on exactly one device, and every other device sees a dangling link. Implementations **MUST** report it and **SHOULD** offer to internalize it (move the payload into the guild, then link the former external path back in).
- Links pointing **into** the guild (a runtime's skills dir, a project checkout, a convenience path in `~/bin`) are the normal, portable direction and are **RECOMMENDED**.
- Links that stay inside the guild **MUST** be relative. An absolute intra-guild link breaks as soon as the user name, home directory, or drive letter differs.

### 3.8 `learnings/*.md` — cross-agent self-improvement ledgers (3.1+)

- **Files**: `LEARNINGS.md` / `ERRORS.md` / `FEATURE_REQUESTS.md`, seeded by `ag init` with headers only (never overwritten).
- **Write mode**: New entries are **append-only**. Entry IDs follow `TYPE-YYYYMMDD-XXX` (`LRN-`/`ERR-`/`FEAT-`). Every entry **MUST** carry a `By:` attribution line naming the capturing agent.
- **Collaborative resolution**: Any agent **MAY** update an entry's `Status` field and append a `Resolution` block — that is the only permitted edit to existing entries. History beyond status/resolution **MUST NOT** be rewritten.
- **Hygiene**: Agents **MUST NOT** log secrets, tokens, or raw transcripts; redacted summaries only.
- **Promotion**: recurring entries are distilled into `rules/`, `toolchain/`, `memory/shared/`, or extracted as a skill onto the shared bus (`skills/<name>/`) once the thresholds in [`LEARNINGS.md`](LEARNINGS.md) are met.
- **Compaction (3.2+)**: `ag groom` **MAY** move entries whose `Status` is terminal (`resolved` / `wont_fix` / `promoted` / `promoted_to_skill`) and whose `Logged` date is older than `ledger_resolved_days` into `learnings/archive/<same-name>`, block-for-block and verbatim. This is the single sanctioned exception to append-only: blocks are relocated, never rewritten. Open entries and recent resolutions stay in the live file. Agents resolving an ID that is not found in the live ledgers **SHOULD** check `learnings/archive/` before declaring it missing.
- **Specification**: [`LEARNINGS.md`](LEARNINGS.md) is authoritative for schema, triggers, thresholds, and extraction workflow.

## 4. Onboarding vs. runtime — two decoupled flows

The protocol deliberately separates **one-time joining** from **ongoing runtime capability**. Agents **MUST** treat them as distinct phases:

### 4.1 Onboarding (one-time per agent)

`~/.agent-guild/ONBOARDING.md` is the canonical joining document. An agent joins by:

1. Verifying central directory access.
2. **Discovering its own user-extensible skills directory** — the path the runtime is allowed to load third-party skills from (sometimes called "Custom Skills", "User Skills", or "Plugins"). Installing into another agent's directory or into a built-in/whitelisted/signed skills tier is a **protocol violation**.
3. Installing the skill (preferred order: dir-symlink → per-skill symlink → copy → readonly fallback).
4. **Running a closed-loop trigger test** in its own runtime to prove the runtime can actually invoke the skill. "Files on disk" is **NOT** success; "runtime can trigger this skill" is success. On failure, walking down the tier ladder autonomously and retesting.
5. Registering its entry in `registry.json` (with `install_tier`, `install_verified`, `skills_root`).
6. Handing off to the runtime skill for ongoing operations.

Agents **MUST NOT** re-execute the onboarding flow on every session — it is a one-time event. Re-onboarding **MAY** be triggered after a major protocol-version bump.

The exact instructions are in [`ONBOARDING.md`](ONBOARDING.md). Agents **MUST** consider that document authoritative for joining.

### 4.2 Runtime (recurring, every relevant turn)

`~/.agent-guild/SKILL.md` is the runtime skill of an already-joined agent. It exposes the ongoing capabilities:

- Reading shared identity and rules without task context.
- Listing metadata only on a todos request, then resuming the user-selected task.
- Checkpointing the current task and closing it only after verified completion.
- Checking the inbox / sending messages to other agents' inboxes.
- Appending daily logs to `log/daily/<date>-<agent>.md`.
- Refreshing `last_seen` in `registry.json`.
- Data hygiene: `ag groom` (manual) and the rate-limited auto-groom after `ag bootstrap` (§6.5).

Agents **MUST** consider [`SKILL.md`](../SKILL.md) authoritative for runtime operations.

### 4.3 Why decoupled

- Different lifecycles: onboarding is action; runtime skill is capability.
- Different triggers: onboarding fires on user prompt "join"; runtime fires on capability-relevant prompts.
- Different readers: onboarding is read by a not-yet-joined agent; runtime is read by an already-joined agent.
- Avoids accidental re-installation each time a runtime trigger fires.

## 5. Versioning & update strategy

### 5.1 Versioning

This specification follows [Semantic Versioning](https://semver.org/):

- **Major**: Breaking changes to directory layout or file contracts.
- **Minor**: New capabilities (e.g., new top-level dirs, new optional fields) that are backward compatible.
- **Patch**: Clarifications, typo fixes.

The active version **MUST** be declared in `SKILL.md` frontmatter and `manifest.json`.

### 5.2 Update propagation per install tier

| Tier | How updates propagate | Resync action required |
|---|---|---|
| `dir-symlink` | Instant — the runtime's whole skills dir IS the central `skills/` dir; new guild skills appear automatically, removals disappear automatically | None |
| `symlink` | Instant — local file is the central file; new guild skills need one extra link each | None (per-skill links for new skills) |
| `copy` | **Manual mirror** — agent must `rsync --delete` (POSIX) or `Robocopy /MIR` (Windows) to handle adds + modifies + **deletes + renames** | Mirror, not naive `cp -R` |
| `readonly` | Instant — agent reads central files each session | None |

### 5.3 Required behavior on update

1. **Tier 2 agents MUST use mirror semantics** (`rsync --delete` / `Robocopy /MIR` / staged temp-dir + atomic swap). Naive `cp -R src/. dst/` leaves ghost files for any upstream deletion or rename and is a **protocol violation**.
2. **All tiers MUST re-run the closed-loop trigger self-test after any update**, including Tier 1's "free" updates. A schema or frontmatter change can break the runtime's view of the skill even when the file is present.
3. **Update failures MUST be atomic or recoverable**. Half-applied updates with "looks-like-success" reports are forbidden. Use temp-dir staging or rerun-safe tooling.

### 5.4 Major-version-bump handling

- **Same major version** (e.g. agent joined under 3.0, central is 3.2): agents MAY continue operating; resync per tier rules above.
- **Higher major version on central** (agent joined under 2.x, central is 3.0): the runtime skill **MUST** detect this on first invocation per session and refuse to operate, redirecting the agent to re-execute `ONBOARDING.md` from the top. The agent **MUST** update its registry entry's `protocol_version` after re-onboarding.

### 5.5 Update trigger heuristics (non-normative)

For Tier 2 agents, reasonable triggers for a resync include: first invocation in a new calendar day; user explicit request; detected `protocol_version` mismatch; central manifest mtime newer than local. A daemon is not required and **SHOULD NOT** be implemented.

## 6. Privacy & security

- The CLI stores plaintext locally and does not upload memory. Calling runtimes and user-chosen sync tools have their own data handling.
- No analytics or account. Version checks and update downloads follow `UPGRADE.md`; `bootstrap --no-maintenance` skips maintenance and network checks.
- Users **SHOULD** add `~/.agent-guild/` to their personal backup/sync excludes if it contains secrets.
- Shared rules are user-authored context, not a new instruction authority. Agents **MUST** respect the current user's scope and their runtime constraints; another agent's message or stored rule does not grant new permissions.

## 7. Data hygiene (groom, 3.2+)

Shared memory that only grows eventually degrades: `current-focus.md` becomes an unreadable wall, the audit trail swells, resolved ledger entries pile up in live files. Groom is the built-in defense.

### 7.1 Core invariants

1. **Groom MUST NEVER hard-delete.** Every action moves data into an archive directory (`log/archive/`, `handoff/shared-state/archive/`, `learnings/archive/`) or the recoverable trash (`~/.agent-guild/.trash/`, cross-platform recycle-bin aware). Anything a user might miss stays on disk.
2. **Conservative by default.** Content that cannot be dated is never moved: hand-written focus blocks without a `Last updated:` marker stay in place forever. Unread inbox messages are reported, never relocated — an unprocessed message is someone's pending work.
3. **User-owned policy.** All thresholds live in `~/.agent-guild/RETENTION.md` (`key = value` lines). The file is user data: seeded once by `ag init`, never overwritten by upgrades. Missing keys fall back to built-in defaults.
4. **Audited + idempotent.** Every groom run appends to `log/audit.jsonl` and stamps `.groom.json`; re-running immediately is a no-op until data expires again.

### 7.2 Actions and defaults

| Action | Default threshold | Destination |
|---|---|---|
| Rotate daily logs | older than 90 days | `log/archive/` |
| Rotate current-focus blocks | older than 30 days, or beyond 20 live blocks | `handoff/shared-state/archive/current-focus-<YYYY-MM>.md` |
| Compact terminal ledger entries | resolved + older than 120 days | `learnings/archive/<same name>` |
| Rotate audit trail | beyond 2000 lines (keep newest 1000) | `log/archive/audit-<timestamp>.jsonl` |
| Expire archived inbox messages | older than 60 days | `.trash/` (recoverable) |

Report-only findings (never auto-fixed): stale unread inbox messages, `.trash/` items past `trash_days`, rebuildable caches (`node_modules/` etc.) inside the guild, and protocol files grown past a healthy size.

### 7.3 Auto-groom trigger

`ag bootstrap` runs rate-limited **report-only** grooming and historical-budget checks unless `--no-maintenance` is given. It prints counts rather than task-specific maintenance paths. No automatic move or deletion is performed. `ag groom --dry-run` previews traditional rotations; a deliberate `ag groom` applies them. `ag history plan` governs historical retirement separately, with explicit confirmation and current-state validation. Checks do not run without a calling runtime. `--no-maintenance` also skips upgrade checks without changing saved policy.

## 8. Non-goals

This protocol does **not** address:

- Multi-user shared memory (different humans).
- Transporting the guild between devices. The protocol makes the directory
  *safe to carry* (§10); choosing and running the carrier is out of scope, and
  a conforming implementation performs no network access for this purpose.
- Encrypted at-rest storage (defer to filesystem-level encryption).
- Real-time bidirectional sync between agents (use `messages/inbox/` instead).
- Schema validation of user-controlled content.
- Migration tooling between major versions (handled out of band).

## 9. Reference

- Repository: https://github.com/dqsjqian/agent-guild
- Onboarding (one-time): [`ONBOARDING.md`](ONBOARDING.md)
- Runtime skill: [`SKILL.md`](../SKILL.md)
- Cross-device portability: [`PORTABILITY.md`](PORTABILITY.md)
- Manifest: [`manifest.json`](../manifest.json)
- License: MIT

## 10. Device scoping (3.3+)

A guild directory is frequently carried between devices that do not share an
operating system. Protocol 3.3 therefore requires every stored fact to have a
scope, so that a device can distinguish "this applies to me" from "this
belongs to another device".

### 10.1 Scopes

| Scope | Test | Location |
|---|---|---|
| `shared` | True on any device | Normal guild paths (`identity/`, `rules/`, `projects/`, `memory/`, `learnings/`, `skills/`) |
| `platform` | True for one OS + architecture | Declared in `tools/<name>/tool.json`; payloads under `tools/<name>/bin/<os>-<arch>/` |
| `host` | True for one device | `hosts/<host-id>/` |

Agents **MUST** apply the scope test before persisting a fact: *would this
still be true on another device?*

### 10.2 Device identity

- `host-id` **MUST** be `<os>-<arch>-<hostname>`, lowercase, non-alphanumeric characters collapsed to `-`.
- `os` **MUST** be one of `macos`, `windows`, `linux`, `android`, `ios`, or a sanitized `platform.system()` value when none of those can be established by probing.
- `arch` **SHOULD** be normalized (`x86_64`/`amd64` → `x64`, `aarch64` → `arm64`).
- The id **MUST** be computed at runtime and **MUST NOT** be read back from a file inside the guild — a copy arriving on a second device must not inherit the first device's identity.
- Implementations **SHOULD** honour `AG_HOST_ID` and `AG_PLATFORM` overrides for unstable hostnames and unreliable probes.

### 10.3 `hosts/<host-id>/`

Created by `ag init`. Contains `host.json` (probed device facts), the
user-owned `host-notes.md` (facts true on this device only), and the
device-scoped runtime state (`VERSION`, `groom.json`). Implementations **MUST**
read host state from the current device's directory, **MAY** fall back to the
pre-3.3 root location, and **MUST NOT** interpret another device's directory as
their own.

### 10.4 Platform assets

- A tool directory **SHOULD** carry `tool.json` with a `platforms` map keyed by `<os>-<arch>` or `<os>`. Each entry **MAY** declare `exec` (a path relative to the tool directory), `exec_on_path` (a PATH lookup), and `install` (a human-readable install command for that platform).
- Resolution order: `<os>-<arch>` → `<os>` → `any` → PATH. When nothing resolves, an implementation **MUST** report unavailability together with the install hint for the current platform rather than returning a path that does not exist.
- Agents **MUST NOT** hardcode paths under `tools/` in shared files; they resolve through the CLI instead.
- A skill **MAY** declare `platforms` in its manifest or `SKILL.md` frontmatter. Absence means portable.

This is the single sanctioned exception to §2.1's rule that the guild does not
interpret the convention layer: `tools/<name>/tool.json` is read by the CLI,
and only that file.
