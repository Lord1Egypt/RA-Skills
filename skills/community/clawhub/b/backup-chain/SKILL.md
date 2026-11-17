---
name: backup-chain
description: "Fenced, hash-chained workspace backups: tarball snapshots carrying a monotonic generation counter and parent sha256 inside each archive, an append-only external ledger (file or user-supplied command — no platform code), gated builds (member presence, manifest roundtrip, sha256 receipt, restore drill), per-member verified restore, a witness layer (compressed decision traces per generation, operator acks, a witnessed ack policy for chains that run ackless by decision, restore/drill event lines — witnesses, never gates), and opt-in curation (per-member excludes, custody-preserving eviction, advisory dead-weight detections). Use whenever the user wants to back up, snapshot, or checkpoint a workspace/project so a crash, wipe, sandbox reset, or rollback can be recovered from; to build or register a backup; to verify, drill, or restore/heal from an archive; to record why a generation was made (decision trace, chain of thoughts, reasoning provenance) or acknowledge having checked one; to prune, slim, evict, or curate chain members without losing custody; or mentions backups, vault, chain head, generations, fencing, restore drill, stale handoff, dead weight, or wipe recovery — even if none of those exact words are used. Do not use for single-file copies, git/version-control workflows, or cloud-sync setup: this skill is deliberately platform-agnostic and contains no upload code — off-site distribution belongs to the user."
---

# backup-chain v1.3.2

Crash- and wipe-resilient workspace backups built on six invariants learned the
hard way. A chain, not a pile of copies: every archive knows its generation and
its parent's hash, an append-only ledger outside the failure domain remembers
both, and no archive counts as "verified" until a restore drill has passed.
On top of the chain sits a **witness layer** (v1.1): compressed decision
traces per generation, operator acknowledgments, a **witnessed ack policy**
(v1.2 — a chain that runs ackless by decision says so in the same ledger an
ack would live in), and custody event lines —
evidence written at rest, never gates. And on top of that sits a **curation
layer** (v1.2): per-member excludes, custody-preserving eviction, and
advisory dead-weight detections — all of them options, none of them defaults,
because no two workspaces look alike and no agent using this skill owes the
universe a side bucket.

## Permissions

- **filesystem read**: the configured project root and the archive paths passed
  on the command line. Enforced, not assumed: a nested symlink whose resolved
  target leaves the project root is skipped with a warning, so archive
  content cannot escape the boundary through a link planted inside a member
  directory.
- **filesystem write**: `<root>/.vault/` (config, ledger file, last-build
  receipt), the configured output dir (tarballs + `.sha256` receipts), and
  `restore --target` — never without an explicit `--target`.
- **file modes (1.3.0/1.3.1)**: archives, their `.sha256` receipts and any
  stow copies are created owner-only (0600) by default, applied verbatim —
  the ambient umask neither widens nor narrows an explicit `--archive-mode`.
  Widen deliberately per invocation (`--archive-mode`); the persistent
  `archive_mode` config key may narrow only — a workspace-supplied value
  carrying group/other bits is refused (rc 2), because config is adversarial
  input (audit T09). exec/setuid/sticky modes are refused for both origins.
  See `references/SECURITY.md`
  § Archive file modes and `references/RESIDUAL_RISK.md` item 16.
- **config path boundary (1.0.5/1.0.6)**: `.vault/config.json` is workspace-
  contributed state and adversarial input — it may propose, the invocation
  root disposes. The stored root is pinned to the invocation root (`realpath`
  equality; a config claiming another directory is refused, so a planted
  config cannot redirect what gets read), member paths are re-validated at
  load (`..`/`~`/absolute refused), `chain_name` must stay a safe filename
  component, `output_dir` must stay inside the workspace (symlinked
  output dirs that resolve outside are refused before anything is created
  — ONE shared containment guarding build and evict alike since 1.3.2),
  and the file-ledger destination must *resolve* inside the workspace —
  absolute, traversing, or symlinked-out paths refuse to append without
  the operator's `--allow-external-ledger` (1.0.6; in-root ledgers never
  consult it). External archive destinations remain a per-invocation
  operator choice: `--output` (build), `--stow-to`/`--stow-cmd` (evict).
- **subprocess**: tarfile/sha256 are in-process; the ONLY external execution
  is (a) the user-configured ledger command adapter (git-hook trust class,
  refuse-by-default via `--allow-cmd-ledger`) and (b) the v1.2 stow command
  passed per-invocation as `--stow-cmd CMD` — the operator's own voice on
  the CLI, never read from config, run as an argv vector (`shell=False`)
  with archive bytes on stdin, announced on stderr. Neither can fire from a
  planted config on a routine subcommand.
- **network: false** · **eval/exec: false**.
- **file content reading: hashing only** — member bytes are read to compute
  sha256 and streamed through archives; never parsed, logged, or transmitted.

## When to use

Use when **all** of these hold:

- the workspace contains files whose loss would be **costly or irreplaceable**
  (credentials, skills, long documents, derivation trails, worklogs), and
- the environment has a **real failure class beyond your control** — sandbox
  resets, dotdir rollbacks, storage rollbacks, platform-side wipes, and
- recovery must be possible **by a later session with no memory** of this one.

Do **not** use when any of these hold:

- **Version control suffices** — if the history lives in git and the remote is
  trusted, git already solves ordering and integrity
- **Single-file copies** — "copy this file somewhere safe" needs no protocol
- **Secrets without a plan** — archives may contain credential files; if the
  user has no private storage for them, read `references/SECURITY.md` first
- **The user just wants cloud sync** — this skill has no upload code by design

## The six invariants

1. **Ordering is asserted, never inferred.** "Newest" by mtime or filename is a
   claim by whatever last touched the inode. Each archive carries a monotonic
   `generation` integer inside a manifest that lives INSIDE the tarball. Stale
   restores are refused by comparison, not guessed away.
2. **The chain is hash-linked.** Each manifest records `parent_sha256` — the
   hash of the previous generation's archive. Parent resolution order: ledger
   entry first, local archive with matching embedded manifest second, filename
   guessing never.
3. **The ledger lives outside the blast radius.** An append-only record of
   `gen / sha256 / parent / built / file` lines. If the workspace and its
   archives can be destroyed together, the ledger must not be destroyable with
   them. The skill ships three adapters — `none`, `file`, `command` — and
   knows nothing about any platform: a `command` adapter is two user-supplied
   command lines (read / append, executed argv-style behind an explicit
   `--allow-cmd-ledger` opt-in), so any append-only channel the user has
   (a gist, a forum post, a git branch, a database row) works unchanged.
4. **A build is not done until a drill passed.** Member presence gate →
   manifest roundtrip → sha256 receipt → re-read every member from the
   archive → hash-compare against the manifest. An archive that was never
   read back and re-hashed is a hope, not a backup.
5. **Restore is per-member, verified.** Bulk extraction has a documented
   failure class: exits 0, writes nothing (observed twice in production with
   patched sandbox environments). This skill never bulk-extracts. Every member
   is streamed out individually and its sha256 checked against the manifest's
   member map — so restores verify even when the source files are gone.
6. **Fencing failures are loud or refused, never silent.** Unreachable ledger
   → proceed marked `SKIP (unverified)`. Older archive than the ledger head →
   refuse (stale handoff). A clearly marked untested solution is more useful
   than a falsely verified one; a heroic retry that overwrites newer state is
   worse than either.

## The witness layer (v1.1)

Guards are checked at invocation — and the adversary attends the invocation.
Witnesses are written at rest, next to the artifact, and read later. The
witness layer adds three of them, none of which gate anything:

- **Decision trace (`cot`)** — why a generation was decided, compressed to a
  bounded schema and written at decision time: `--cot-trigger` (one of
  `schedule | pre-migration | pre-risky-op | post-heal | manual | anomaly`),
  `--cot-belief` (≤140 chars: what was believed about workspace state),
  `--cot-risk` (≤80 chars: what was consciously accepted), `--cot-falsifier`
  (≤80 chars: one checkable claim that, if false, indicts the reasoning).
  Stored in the manifest (inside the archive — a rollback cannot edit it
  without breaking hashes) and prefix-digested into the ledger line (`cot=`),
  so the why survives even when the archives do not. Overflow **refuses** the
  build; traces are never truncated (truncation silently edits reasoning).
  `verify` compares the two copies — agreement is evidence, disagreement is a
  loud alarm, never a refusal.
- **Operator ack (`ack GEN [NOTE]`)** — a human saying "I have seen gen N and
  its drill receipt." Written when the operator actually looks, never on a
  schedule; attests the looking, not the believing. Refuses unknown
  generations and unreachable ledgers; adapter `none` has no witness layer to
  ack into. The ack is the second, independent witness: silent forgery of
  history now requires subverting the chain *and* the operator in
  coordination — a probability shift, not a guarantee, and the docs never
  claim otherwise.
- **Ack policy (`ack-policy off|on`, v1.2)** — acks are witnesses, not
  gates, so disabling them is a legitimate choice (a chat-only operator who
  cannot run a shell, for one). What it may never be is **traceless**:
  `ack-policy off --note WHY` appends `event=ack-off` to the same ledger an
  ack would live in, and `ack-policy on` appends `event=ack-on` — both
  refuse when the ledger is unreachable or absent (adapter `none`
  included), because an un-witnessable policy change is exactly the silence
  this command exists to prevent. While off, `ack GEN` refuses and points
  at the recorded decision; `status` shows the policy; `verify` attributes
  the absence of acks to the policy, never to neglect. Historical acks stay
  on record. Builds, drills, and restores are untouched (witness, not
  gate).
- **Event lines** — `event=restore gen=N ts=… target=…` after a successful
  restore, `event=drill gen=N ts=…` after a standalone drill. The restore act
  used to be the one consequential thing a chain never remembered. Verifies
  are deliberately *not* recorded: a verify is a read, repeatable at zero
  cost, and reads don't belong in an append-only witness.

All three travel through the same ledger adapters and inherit every audit
consent boundary unchanged. None of them move `next-gen`.

## The curation layer (v1.2) — options, never defaults

The founding constraint, applied twice: an agent using this skill may have no
storage beyond its own, and no two workspaces look alike. So every piece of
this layer is opt-in, and silence is exactly the old behavior.

- **Per-member excludes** — `member add PATH --exclude PATTERN` (repeatable;
  fnmatch against the path relative to the project root and the basename).
  The ONLY built-in patterns remain the self-exclusion class (`*.tar.gz`,
  `*.tar.gz.sha256`, `*.part`) so the chain never swallows its own archives.
  An excluded directory prunes its whole subtree — one pattern now means the
  subtree, not just the entry. Excludes are silent holes by nature: review
  them with the member list (`member list` shows them), and let the
  detections below show you the weight that remains.
- **Eviction with custody** — `evict PATH --stow-to DIR|--stow-cmd CMD
  [--note NOTE]` removes a member from the chain only after its content has
  landed somewhere: packaged with a per-member hash map into
  `<chain>-evict-g<HEAD>-<ts>-<name>.tar.gz` + receipt, handed to the
  destination, hash-verified for `--stow-to` (a failed roundtrip refuses the
  eviction — the member stays tracked), or piped to your own upload command
  via `--stow-cmd` (success = its exit code, claimed not verified). An
  `event=evict` witness line records the act. Without a destination the
  command refuses: silent custody loss is what it exists to prevent
  (`member remove` stays the deliberate silent drop). Files on disk are
  never touched. The intermediate package lands in the configured
  `output_dir` under the same realpath containment as build (1.3.2): an
  output dir resolving outside the workspace refuses the eviction before
  anything is written — package, receipt, or directory.
- **Build-time custody hand-off** — `build --stow-to DIR` / `build
  --stow-cmd CMD` hand the finished, drill-passed archive to the same
  destinations and record `event=stow`. Failures warn; they never gate —
  the archive exists either way. With neither flag, builds print nothing
  about stow at all.
- **Detections (advisory, never gates)** — every build prints `DETECT`
  warnings on stderr for the dead-weight classes a real chain actually died
  of: archive growth vs the parent generation (the quiet creep toward a size
  ceiling), identical content riding under several member paths, and the
  largest members entering this archive. `status` shows raw member and
  archive totals. Thresholds are tunable in the config (`detect`:
  `growth_pct` 50, `growth_mb` 4, `archive_mb` 32; `enabled: false` silences
  the layer); they never change an exit code.

## Quickstart

```bash
BC="python3 <skill-dir>/scripts/backup_chain.py"

# one-time setup (from the project root)
$BC init --name myproject --ledger file
$BC member add worklog.md --critical
$BC member add skills/
$BC member add download/        # tarballs/receipts inside are auto-excluded
$BC status                      # review the member list

# every build
$BC build --carries "what changed this turn" \
  --cot-trigger schedule --cot-belief "tests green, tree clean" \
  --cot-risk "db/ excluded by design" \
  --cot-falsifier "members list matches status output" \
  --register   # --register appends to the ledger
# → prints the ledger line even without --register (for manual posting)

# when you actually look at the chain (witness, never required)
$BC ack 12 "drill receipt read, matches expectations"

# if your operator cannot ack at all (chat-only, no shell), say so on the
# record once — the no-ack chain then explains its own silence
$BC ack-policy off --note "chat-only deployment; human signal lives in chat"

# curation, when the chain needs slimming (all opt-in)
$BC member add skills/ --exclude skills/design --exclude "*.log"
$BC evict old-bulk/ --stow-to /mnt/side-bucket --note "evicted at gen 12"
$BC build --carries "slimmed" --register --stow-to /mnt/side-bucket

# recovery
$BC verify download/myproject-g12.tar.gz
$BC check download/myproject-g12.tar.gz       # pre-restore fencing gate → JSON
$BC restore download/myproject-g12.tar.gz --target /fresh/workspace
$BC recheck 12                                # post-apply receipt
```

The ledger is what makes a wipe survivable: after a total loss, `next-gen`
still respects the ledger's highest generation, `check` refuses stale archives
the ledger never registered, and `verify` can authenticate a pulled archive
against a ledger entry even when nothing local survives.

## Commands

`<BC>` = `python3 <skill-dir>/scripts/backup_chain.py [--root DIR]`.
Default root is the current working directory; config lives at `<root>/.vault/config.json`.

```bash
# setup
$BC init [--name NAME] [--output-dir DIR] [--ledger none|file|command]
         [--ledger-file PATH] [--read-cmd CMD] [--append-cmd CMD] [--force]
$BC member add PATH [--critical] [--exclude PATTERN]...
          | member remove PATH | member list
$BC evict PATH (--stow-to DIR | --stow-cmd CMD) [--note NOTE]
          # [--archive-mode MODE]; custody-preserving member removal (v1.2;
          # refuses without a destination; never touches the files on disk)

# build and register
$BC next-gen                       # print next generation: max(local, ledger)+1
$BC build [--carries NOTE] [--cot-trigger T] [--cot-belief B]
         [--cot-risk R] [--cot-falsifier F] [--label LABEL]
         [--register] [--output PATH]
         [--archive-mode MODE]              # v1.3.0, default 0600 owner-only
         [--stow-to DIR | --stow-cmd CMD]   # v1.2, opt-in custody hand-off
$BC ledger-line TARBALL [--append] # print (or append) the ledger entry
$BC ack GEN [NOTE]                 # operator acknowledgment (v1.1 witness)
$BC ack-policy [off|on] [--note W] # ack policy; every change is witnessed
                                   # (event=ack-off / event=ack-on, v1.2)

# inspect and verify
$BC status                         # local chain head, ledger head, acks, members
$BC verify TARBALL                 # sha vs receipt + ledger entry + trace agreement
$BC drill TARBALL                  # standalone restore drill (+ witness event)

# fencing and restore
$BC check TARBALL                  # → {"decision": "restore"|"refuse"|"skip", ...}
$BC restore TARBALL --target DIR [--overwrite] [--dry-run] [--force]
$BC recheck GEN                    # → {"decision": "ok"|"stale"|"skip", ...}
```

### Exit codes

`0` success · `1` failure (gate, verification, drill, or restore mismatch —
the message says which) · `2` refused (fencing refuse, overwrite without
`--overwrite`, dangerous target). Refusals matter: `build && next_thing` must
not proceed on the assumption a backup exists.

### Ledger adapters

| adapter | read | append | notes |
|---|---|---|---|
| `none` | — | — | local-chain fencing only; every gate result says so |
| `file` (default) | read `.vault/ledger.log` | append + fsync | a ledger inside the workspace is NOT wipe-safe — use it for testing, or keep the real ledger elsewhere via `--ledger-file` (then pass `--allow-external-ledger` on every invocation that touches the ledger) |
| `command` | `--read-cmd CMD` (stdout = ledger text) | `--append-cmd CMD` (entry on stdin) | your platform, your credentials, your identity filtering — the skill never learns any of it |

Command-adapter rules: the configured command is parsed with `shlex` and
executed as an argv vector — no shell — with the entry text piped to stdin for
appends. Shell features (pipes, redirects, globs) are inert unless you name a
shell yourself (`sh -c '…'`), in plain sight in the WARN preview. Execution is
refuse-by-default: pass `--allow-cmd-ledger` on any invocation that should run
the adapter. The flag is per-invocation, so a planted config cannot fire on a
routine `status`/`check`/`restore`; automation passes it only in scripts you
reviewed. Without the flag, the read path reports unreachable-with-guidance
and registration fails loudly. This is user-owned configuration in the
git-hook trust class — review it before `init`. If the channel is shared,
filter for identity **inside the command** (e.g. `grep` for your handle),
because the ledger parser accepts any line that looks like an entry.

File-ledger boundary rules (1.0.6): the ledger destination in
`.vault/config.json` must resolve inside the workspace — absolute,
traversing, or symlinked-out paths refuse to append without
`--allow-external-ledger` on the invocation (the read path reports
unreachable-with-guidance instead). Containment is resolved via `realpath`
at every use, so a symlink planted after `init` still fails closed.
The wipe-safety setup keeps working: `init --ledger-file /external/path`
chooses the destination in the operator's own voice, and every later
invocation that reads or appends the ledger carries the flag. The two
guards are independent: `--allow-external-ledger` never enables the command
adapter, and `--allow-cmd-ledger` never unlocks external ledger paths.

## Workflow

### Steady state

1. `member add` every path whose loss would hurt; `--critical` ones fail the
   build if missing (others warn).
2. `build --carries "note"` each session (or each turn). Read the printed
   drill result — `drill: PASS` is the whole point.
3. `--register` (or post the printed line by hand) so the ledger head advances.
4. `status` occasionally; keep at least the newest receipt beside its archive.
5. Copy the newest tarball + `.sha256` off-site **yourself** (see
   `references/PROTOCOL.md` § Off-site distribution for the roundtrip
   verification pattern: upload → fetch back → hash-compare → only then call
   it MATCH).

### Wake after a wipe

1. `status` — inventory what survived. Missing `.vault/` is fine; rebuild with
   `init --force` and re-add members.
2. Find the newest archive (local or off-site pull). `sha256sum -c` its receipt.
3. `verify` against the ledger (authenticates even with an empty workspace).
4. `check` — refuse on stale handoff is the protocol working; investigate, do
   not override.
5. `restore --target .` — per-member, hash-verified.
6. `recheck <gen>` — `ok` closes the incident; `stale` means the ledger
   remembers more than you restored (bytes landed, precondition did not).
7. `build` a fresh generation carrying the heal note, so the chain records the
   incident and the cure.

### Witnessing (v1.1)

The ack is worth one operator minute when you look at a chain, and it is
worth nothing if it is ritual. Ack the generation whose drill receipt you
actually read; skip the rest. A trail of honest gaps (generations nobody
acked) is more informative than a wall of rubber stamps — the disagreement
between the automatic witness and the human witness is the alarm this layer
exists to make possible. If your deployment has no human who can ack at all
(chat-only operators, unattended automation), do not leave the gaps
ambiguous: `ack-policy off --note WHY` records the decision once, in the
ledger, and every later reader sees policy where they would otherwise see
neglect. Read `references/RESIDUAL_RISK.md` before adding any further
control to this skill.

## Session-tracker and content provenance

This skill pairs well with a checkpointing skill (e.g. session-tracker) but is
a different layer: the tracker checkpoints **task state** so work resumes; the
chain guarantees **artifact custody** so conclusions survive. Custody is not
validity — a sha256 proves a sentence survived a restore, not that it was ever
right. If your workspace records why conclusions were drawn (route files,
premises, falsifiers), put those route files in the member list so they hash
into the same chain as the artifacts they audit. See
`references/PROTOCOL.md` § Custody vs validity.

## What this skill does not do

- **No network** — no sockets, no HTTP, no upload. Off-site copies are made by
  you; the ledger `command` adapter touches whatever your commands touch.
- **No platform code** — no storage SDKs, no forum clients. Distribution is
  the user's job; verification is the skill's.
- **No secret management** — it will warn when member paths look secret-like
  (credentials, tokens, keys) and hash them like anything else. Whether that
  is safe depends entirely on where you send the archives. Read
  `references/SECURITY.md` before backing up secrets.
- **No content reading** — bytes are hashed and streamed, never parsed or logged.
- **No daemon, no scheduling** — a chain you forget to extend is a pile.
  Pair it with whatever scheduler you already have.

## Files

| Path | Purpose |
|---|---|
| `<root>/.vault/config.json` | Chain configuration (members, ledger, output dir) |
| `<root>/.vault/backup-chain-dir` | Ownership marker |
| `<root>/.vault/ledger.log` | Default file-ledger (append-only) |
| `<root>/.vault/drill/` | Legacy (<= 1.2.1): created empty by the drill. No longer created or used — the drill reads back in memory |
| `<root>/.vault/last_build.json` | Receipt of the last build (gen, sha, gates) |
| `<output-dir>/<name>-g<GEN>[-<label>].tar.gz` | Archives (generation in the NAME is a label; the manifest is authoritative) |
| `<output-dir>/<name>-g<GEN>[-<label>].tar.gz.sha256` | Hash receipts |
| `<output-dir>/<name>-evict-g<HEAD>-<ts>-<name>.tar.gz` | Eviction packages (v1.2; own manifest, own receipt; never match the build prefix) |

## Installation

```bash
cp -r backup-chain/ <your-skills-dir>/backup-chain/
python3 <your-skills-dir>/backup-chain/scripts/backup_chain.py --help
bash <your-skills-dir>/backup-chain/tests/test_backup_chain.sh
```

Python 3.8+, standard library only, no dependencies, no network.

## Further reading

- `references/PROTOCOL.md` — threat model, the six invariants argued properly,
  the witness layer (v1.1), gate list, fencing state machine, off-site
  distribution patterns, and the incident classes behind each rule
- `references/SECURITY.md` — secrets in archives, ledger-adapter trust, restore
  overwrite discipline, witness-layer hygiene, audit notes
- `references/RESIDUAL_RISK.md` — the acceptable-risk line: what this skill
  does NOT protect against, and the standing rule every future control must
  satisfy
- `references/METHOD.md` — how breakage gets into this skill under efficiency,
  control and incentive pressure, what each way of framing a review leaves
  unseen, the admission rules for changing it, and the sink-inventory
  tripwire (`tests/check_sinks.py`) that enforces part of that in code
- `references/CHANGELOG.md` — version history for the current line (1.2.0
  onward); pre-1.2.0 history lives in `references/CHANGELOG-ARCHIVE.md`
