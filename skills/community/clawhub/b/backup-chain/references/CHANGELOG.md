# Changelog — backup-chain

Current line: 1.2.0 onward. Pre-1.2.0 history (1.0.0-1.1.1) lives in
[CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md), moved byte-faithfully at 1.3.0
so each half stays fully inspectable; no entry was edited in the move.

## 1.3.2 — 2026-10-12

Audit-response release, one change: the output-dir containment build has had
since audit round 4 now guards evict too — one shared gate instead of two
code paths that can diverge. Found by the ClawHub security audit of the
published 1.3.1 package (T09 · Insecure Skill Coding Practices, Warning,
re-scan of 2026-10-11): "Eviction Output Can Escape the Workspace Through a
Symlinked Output Directory". The T09 label's rounds on this skill have each
been a different root cause under one pattern — workspace-controlled
configuration doing something the workspace should not be allowed to do
(1.0.3 shell execution via ledger config, 1.0.4 backup-root redirection,
1.0.5 file-ledger append outside the workspace, 1.2.0 predictable staging
names, 1.3.0 permission widening) — and this round is the pattern
reappearing through code that predates one of the fixes: evict was added in
1.2.0 and inherited the pre-round-4 output handling.

- **Fixed — evict wrote the eviction package and its receipt wherever the
  configured `output_dir` resolved, symlinked components included.** The
  round-4 gate (1.0.5) hardened build's output_dir with `realpath` +
  `commonpath` containment; evict's handler kept the
  `outdir = output_abs(cfg); os.makedirs(...)` shape, which the lexical
  config validation passes but a planted symlink defeats. A
  lexically-inside config value with a symlinked component therefore
  carried the credential-bearing package — eviction exists to move
  criticals — and its receipt outside the workspace, rc 0, custody
  completed. Reproduced against the shipped 1.3.1 package before the fix:
  symlinked output_dir → package + `.sha256` land outside, member
  untracked. Since 1.3.2 build and evict both call ONE shared containment
  helper (`contained_output_dir`) BEFORE makedirs or staging — a refusal
  leaves nothing behind, not even a directory — and build's own gate moved
  earlier to the same before-makedirs position (strictly stronger than
  round 4; build's refusal message and the `--output` escape hatch are
  unchanged).
- **Behavior change, loud and narrow:** `evict` with an output_dir that
  resolves outside the workspace now refuses (rc 1, same gate class as
  build) naming the resolved escape and the per-invocation remedy
  (`--stow-to`/`--stow-cmd`). Legal in-root output_dirs are unaffected.
  No new flag: build's `--output` has no evict equivalent because evict's
  custody hand-off IS the per-invocation escape — the intermediate package
  was never meant to live outside the workspace.
- **Tests:** suite 386 → 400 (new T44 family, 14 assertions: evict refusal
  rc/message/remedy, nothing written through the link, member stays
  tracked, check-before-makedirs via a fresh subpath under a symlinked
  parent, build/evict shared-prefix parity with per-command remedies, and
  the in-root regression path; an idempotent member re-add keeps the family
  mutation-readable). Mutation check against the shipped 1.3.1 package:
  392 passed / 8 failed — all 8 in T44 (the escape, its refusal message,
  the external landing, the untrack, the through-link makedirs), none
  elsewhere.
- Scanner noise unchanged from 1.3.1's disclosure: `tests/test_backup_chain.sh:905`
  "dynamic code execution" is the C37 importlib unit test of the
  ledger_append chokepoint (loads our own module by path);
  `scripts/backup_chain.py:173` "obfuscated code" is the 1.2.2 line-break
  character class (the ledger-forgery fix, escape-dense by design).

## 1.3.1 — 2026-10-12

Audit-response release, one change: the trust boundary 1.3.0 built is
extended to the new config key 1.3.0 introduced. Found by the ClawHub
security audit of the published 1.3.0 package (T09 · Insecure Skill Coding
Practices, Warning/Medium, 2026-10-11) — the fourth round this skill has
drawn a T09, each a variant of one pattern: workspace-controlled
configuration doing something the workspace should not be allowed to do
(1.0.3 shell execution via ledger config, 1.0.4 backup-root redirection,
1.0.5 file-ledger append outside the workspace, 1.3.0 permission widening).

- **Fixed — a planted `archive_mode` in config.json could widen archives,
  receipts and stow copies up to 0666.** 1.3.0 accepted the config key and
  capped a planted value at 0666 "at most, visible on the G7 line"
  (RESIDUAL_RISK 16c said so out loud). The audit's counter is the skill's
  own precedent: visibility is not consent — the same argument that closed
  1.0.4's T09 (command-ledger warning → per-invocation opt-in); an operator
  who never runs `stat` never sees the G7 line either. Since 1.3.1 the
  config key may only NARROW the artifacts (any mode with no group/other
  bits — 0000/0200/0400/0600); a value carrying group/other access is
  refused loudly before anything is written (rc 2, naming the value, the
  rule, and the remedy). Widening stays the operator's own per-invocation
  act, echoed on the G7 line: `--archive-mode 0644`. The check lives at the
  single mode-resolution point per command, so build archives, receipts,
  eviction packages and stow copies are covered by one rule; `evict`
  refuses the same way and leaves the member tracked. *New failure
  introduced:* a 1.3.0 deployment that set `archive_mode: 644` (or any
  group/other mode) in config.json must now pass `--archive-mode` on the
  command line — deliberately loud, rc 2, one line explaining why. The T42
  config case was rewritten for the new semantics (604, a widening value →
  400, a narrowing one); the new T43 family pins the boundary itself
  (15 assertions, verified by mutation check to fail against the shipped
  1.3.0 — 12 of them, all in T43, none elsewhere). Suite 371 → 386, all
  green; sink registry unchanged (SINKS OK, 37 calls). Two scanner
  static-analysis notes triaged as noise, for the record: the "dynamic code
  execution" at tests/test_backup_chain.sh:905 is the C37 importlib unit
  test of the `ledger_append` chokepoint (loading our own shipped module by
  path — no remote payload, no eval), and the "obfuscated code" at
  scripts/backup_chain.py:173 is the 1.2.2 line-break character class
  (`\x00…\u2028\u2029`), escape-dense by design — it is the fix for the
  1.2.2 High ledger-forgery finding, not a payload.

## 1.3.0 — 2026-10-12

Adoption release. The 1.2.2 package was audited before adoption by
independent reproduction (suite green, sink tripwire green, and the 22-assertion
mutation check against shipped 1.2.1 reproduced exactly), installed from the
verified package bytes, and only then changed. Three changes, decided in that
audit; no gate, ledger format, or exit-code contract changed.

- **Changed — archives and their receipts are created owner-only (0600) by
  default.** Through 1.2.2 an archive landed `0666 & ~umask` — usually
  world-readable — while SECURITY.md warned that archives can hold secrets,
  and restored members already landed owner-only through the staging
  discipline. The default is now 0600, applied **verbatim**: umask neither
  widens nor narrows an explicit choice, so `--archive-mode 0644` means 0644
  under umask 077, and the G7 receipt line prints the mode that landed.
  Opt-out: `build --archive-mode MODE` / `evict --archive-mode MODE`
  (per invocation) or the persistent `archive_mode` config key; CLI wins
  over config wins over the default. Receipts and `--stow-to` copies follow
  the archive's mode. Modes outside the data-file class (exec/setuid/setgid/
  sticky, anything above 0666) are refused before anything is written, rc 2,
  naming the value's origin. *New failure introduced:* a deployment that
  relied on world-readable archives must now pass the flag or set the config
  key — deliberately loud, one line, in the operator's own voice. Standing
  rule paid in RESIDUAL_RISK item 16; SECURITY.md gains an Archive file modes
  section (and states, for the first time, that restored members land
  owner-only — behavior true since v1.1, previously undocumented).
- **Fixed — two stale drill claims in SKILL.md**, the last survivors of the
  1.2.2 correction pass: the Permissions section still listed ".vault/drill
  staging" under filesystem write, and invariant #4 still said "extract to
  staging", while the script docstring, the G8 gate line, PROTOCOL.md and the
  Files table all correctly describe a read-back that writes nothing. Found
  in the pre-adoption audit — the exact R7 class METHOD.md codifies, missed
  by the same release that wrote R7; recorded here rather than silently
  patched into the published 1.2.2 bytes.
- **Changed — CHANGELOG split.** Pre-1.2.0 history (nine 1.0.x entries, two
  1.1.x entries, ~29.5 KB) moved byte-faithfully to
  `references/CHANGELOG-ARCHIVE.md`; this file keeps the current line
  (~15 KB). The 1.2.1 ClawHub audit recorded a coverage limit (this file too
  large to inspect completely) and the maintainer correctly left the
  reference in place (R4: removing a pointer to dodge inspection is the
  wrong fix). The split is the other half of that answer: both halves now
  sit under the inspection threshold, no pointer was removed, no history was
  edited, cross-pointers run both ways — and it was done in a release that
  was already changing this file, not retroactively on a published,
  hash-verified package.

Tests: 347 -> 371 (T42: 0600 default for archive and receipt, verbatim
application proven under umask 077, config form, CLI-over-config precedence,
boundary refusals with the refusal MESSAGE asserted — not just the exit code,
stow-copy and evict-package modes, refused build writes nothing, and the
restored-member owner-only property pinned). The sink registry row renamed
with the function (set_default_perms -> set_fd_mode) — the tripwire caught
the rename before the registry was updated, which is the friction-by-design
working. Run against shipped 1.2.2 (its script and its registry), 20 of the
suite's assertions fail: the 0600-default family, every --archive-mode path
(rc 2: unknown flag), both refusal messages, the G7 mode line, the
stow/config/evict mode assertions, and the restored-member pin's cascade
(no archive exists there to restore). Two further failures are the T40
registry mutation that targets the renamed row and therefore cannot mutate
the 1.2.2 registry — expected.

## 1.2.2 — 2026-10-11

Independent review of 1.2.1 by adversarial testing. Nothing below was reported
by the ClawHub scan (outcome "Pass"; triage of its findings is at the end of
this entry). Every defect was reproduced against the shipped 1.2.1 before it
was fixed, and every regression test was run against the shipped 1.2.1 to
confirm it fails there. No option, gate, format, default, or exit code changed
for any input that was valid before; one status line changed wording (G8, see
below), and the `.vault/drill/` directory is no longer created.

- **Fixed — ledger forgery via line separators other than `\n`/`\r`
  (High).** The single-line validators (`cot` fields, `ack`, `ack-policy` and
  `evict` notes) rejected `\n`, `\r`, NUL; the readers split with
  `str.splitlines()`, which also splits on VT, FF, FS, GS, RS, NEL, U+2028 and
  U+2029. `ack 1 "x<U+2028>gen=999"` was accepted, written as one physical
  line, and read back as a forged build entry: `next-gen` jumped from 2 to
  1000, and a note of `x<U+2028>gen=1 sha256=<64 hex>` (inside the 120-char
  cap) plants a forged hash for a real generation. The 1.1 witness-layer
  validators were checked against the *writer*; the reader's definition of
  "line" was not. Fixed at three layers (SECURITY.md § Ledger line
  discipline): writers refuse the class and `ledger_append` enforces it at the
  chokepoint; readers split on `\n` only; the new `LEDGER-ANOMALY` alarm makes
  a poisoned line's inertness visible. `has_line_break` is tested exhaustively
  against `str.splitlines()` over all of Unicode, not against a hand-listed set.
- **Fixed — `evict` wrote unvalidated member paths and package filenames into
  the ledger (High, same class).** A member whose *name* contained a newline
  forged a `gen=` line with no separator trick at all. Filename-derived fields
  are now escaped (`%XX`), not refused: the eviction still happens and is
  still witnessed. The package filename component is stripped of control
  characters and separators.
- **Fixed — `--stow-to` followed a pre-planted symlink at the predictable
  archive name and then reported MATCH (High).** The 1.2.1 staging hardening
  covered every temporary file but not the stow copy, a write to a predictable
  *final* name in an operator-chosen directory. `shutil.copy2` reopened the
  pathname, so the archive bytes landed wherever the link pointed, and the
  roundtrip hash read back through the same link falsely confirmed custody.
  The copy is now staged (`mkstemp`, fd-written, fsynced), verified *before*
  taking its final name, and moved with `os.replace`, which replaces a planted
  link rather than following it.
- **Fixed — a failed stow copy left a truncated file under the archive's real
  name.** `stow_to_dir`'s own docstring promised a silent bad copy never
  impersonates custody; only the hash-mismatch path honored it, not an I/O
  error mid-write. Reproduced with a file-size rlimit: 1.2.1 left a 1 MiB stub
  named like the archive; 1.2.2 leaves nothing. Same change as above.
- **Corrected — the restore drill claimed more than it did.** `run_drill`
  hashes members from the decoded archive stream and never wrote into its
  `stage_dir`; yet its docstring said "extract every manifest member to
  stage_dir", `build` printed `members verified in …/.vault/drill`, and
  PROTOCOL.md said G8 "re-extracts every member to staging … this file is
  recoverable." It also ran a recursive `rmtree` on that parameter, safe only
  because both callers passed a tool-owned path. Semantics are unchanged (an
  extract-to-disk drill doubles the I/O and is the operator's decision); the
  claim was brought down to the behavior: the G8 line now reads "N members
  re-read from the archive and hash-verified; nothing written to disk"
  (the `restore drill: PASS` prefix is unchanged), the vestigial
  `rmtree`/`makedirs` are gone, and PROTOCOL/SECURITY/SKILL say "read-back".
  The residual — a drill cannot see a target-filesystem failure — is
  RESIDUAL_RISK item 15.
- **Fixed — `evict` of a member with a long name (~150+ chars) crashed with a
  raw `OSError` traceback.** The package filename embedded the unbounded
  basename. Bounded; and `main()` now turns any remaining `OSError` into a
  one-line `FAIL: I/O error` with the same exit code (1) a traceback gave.
- **Fixed — the shipped test suite failed 3 of 291 assertions when run as
  root** (agent sandboxes, Docker CI): T30 simulated a failing custody
  destination with `chmod 555`, which root ignores, so the one assertion that
  proves "failed custody keeps the member" failed for the wrong reason. The
  destination is now a path beneath a regular file, which fails for every uid.
  Verified green both as root and as an unprivileged user.
- **Added — sink-inventory tripwire** (`tests/check_sinks.py`,
  `tests/sink_registry.txt`, suite test T40; method in `references/METHOD.md`).
  Not a fix for a defect but the control that would have caught the stow one:
  run against 1.2.1's script it reports `BANNED sink shutil.copy2 in
  stow_to_dir`. It inventories every filesystem-write / process-spawn /
  archive-write call by (function, kind, count), refuses pathname-reopening
  writers outright, allow-lists imports (so "no network *code in this
  script*" is checked), bans dynamic features that would hide a sink from the
  scan, and guards the file set of `scripts/`. The tripwire is tested by
  planting each kind of drift. METHOD.md records how this class of defect
  gets in under efficiency, control and incentive pressure and what each way
  of framing a review leaves unseen.
- Stale `v1.2.0` in the script's module docstring corrected.

Standing-rule answers for the new controls (full text: RESIDUAL_RISK items
13–15). *New failures introduced:* refusal of a legitimately-weird note (loud,
rc 2); a cosmetic `%0A` ambiguity in escaped fields; a reader that would merge
records from a channel using other separators; a registry that can be filled in
carelessly; a drill whose limits are now stated rather than implied.
*Duplication:* reader-side split and writer-side refusal overlap on purpose —
the 1.2.1 gap was exactly a writer/reader disagreement. *Loud or silent:* all
fail loud (`LEDGER-ANOMALY`, rc 2/1 with reasons, rc 1 from the tripwire with
the function named).

Tests: 291 → 347 (T37 ledger line discipline, T38 stow staging, T39 evict
hostile and oversized names, T40 tripwire, T41 honest drill, plus a root-proof
T30). Run against shipped 1.2.1, 22 of the new assertions fail: 21 exercise a
defect or a claim, 1 probes code that did not exist there.

Reviewed and found sound, by independent reproduction rather than the bundled
suite: command-adapter and external-ledger consent refusals, `shell=False`
(a `;` in `read_cmd` is inert), `--stow-cmd` reachable only from the CLI and
never from config, restore's symlinked-component refusal, the out-of-root
symlink exclusions (files and directories), and the `mkstemp` staging
primitives themselves.

ClawHub 1.2.1 audit, triaged finding by finding (the page's header says 32; it
lists 25 in detail, all accounted for here): **18** are test fixtures or
changelog prose read as behavior (12 × Tool Parameter Abuse on test
assertions that check things are *refused*; 2 × Anti-Refusal on a sentence
documenting that excludes are silent; Session Persistence on the word "cron"
in a description of what a planted config *could* aim at; 2 × Autonomous
Decision Making on changelog text describing the consent gates; Skill
Enumeration on a dummy `skills/sk1/SKILL.md` fixture). **3** are the documented,
opt-in `subprocess` design (`append_cmd`, `read_cmd`, `--stow-cmd`) — consent-
gated, `shell=False`, kept. **1** (`set_default_perms`) is the read-and-restore
of the process umask: a real but negligible race in a single-threaded CLI, and
the 0666 & ~umask mode is deliberate parity with pre-1.2.1 behavior — unchanged,
named so it is a decision rather than an accident. **2** are not actionable
(Undeclared Tool Scope: skills have no permission-declaration format; Vague
Triggers: broad recall is the intended behavior and the exclusions are
enumerated). **1** is a coverage limit (Ae1: `references/CHANGELOG.md` is too
large for the scanner to inspect completely): recorded, and the reference is
left in place — removing a pointer to evade inspection would be the wrong fix
(METHOD.md R4); condensing the file into current and archived halves is the
maintainer's call.

## 1.2.1 — 2026-10-09

Security hardening: unpredictable staging for every temporary write. No
option, gate, format, or default changed; with no flags passed, every
command behaves exactly as 1.2.0 (the full pre-existing suite passes
unchanged; the suite grows from 271 to 291 assertions, all green).

ClawHub's audit re-scan of 1.2.0 returned the T09 label for a third,
different root cause — and the same scan's own excerpts confirm the
round-3/4/5 consent-gate fixes (command adapter, config path boundary,
external ledger) are intact and remain the design. The new finding,
"Predictable Temporary Files Permit Symlink-Based Writes Outside
Authorized Boundaries" (Warning), is real in our own sink map: temporary
files were created at predictable names beside their destinations —
`.<name>.tmp` for config/marker/receipt/state writes, `<archive>.part`
for build and eviction, `<member>.restore-part` for restore — and the
writes went through path-reopening `open()` calls that follow symlinks.
Anyone who could write to a destination directory (operator-set
`--output`, external ledger path, restore `--target`) could pre-plant
the staging path as a symlink and have the bytes land outside the
boundary the operator chose. v1.2.0's own side-bucket and custody options
made the class worth taking seriously: the number of operator-chosen
destination directories had just grown.

Adopted remediation, per the auditor's suggestions: `tempfile.mkstemp`
in the destination directory (random, `O_CREAT|O_EXCL` — nothing can be
pre-planted at the name), writes through the returned fd (never by
reopening the pathname), fstat regular-file assertion, fsync and
`os.replace` preserved, umask-parity fchmod where the platform allows.
The staging suffix family stays `*.part`, so the self-exclusion default
excludes still shields crash leftovers from re-collection by the next
build (regression-tested both for the new naming and the legacy one).
Regression tests plant symlink decoys at every old predictable staging
name and verify: the decoy target is never written, the decoy itself is
never consumed, the operation succeeds, and no staging leftovers remain.

The standing rule is paid in RESIDUAL_RISK item 12: unpredictable staging
removes an observability signal (watching for predictable staging files
no longer works), and the honest residual stands — an attacker who
controls a destination directory still controls that directory; this
closes the out-of-boundary write primitive, not the trustworthiness of a
hostile directory.

## 1.2.0 — 2026-10-09

The curation layer. Second minor release: no invariant changed, no gate
added, no format broken — everything is additive, and with none of the new
flags passed, every command behaves byte-for-byte like 1.1.1 (asserted by
T31's "default build stays silent about stow" and by the whole pre-existing
suite passing unchanged). Born from a dead-weight audit of the production
chain this skill was distilled from: the chain was quietly creeping toward
its size ceiling, and the audit that slimmed it produced three
generalizations, submitted to the operator with implementation proposals.
The operator's decisions are on the record and shaped everything below:

1. *"We can't expect that an agent using skill would have some storage
   outside of own, so features about side buckets should be under options,
   not default behavior."* — adopted verbatim. There is still no upload
   code; `evict --stow-to|--stow-cmd` and `build --stow-to|--stow-cmd` are
   per-invocation opt-ins, and a build without them prints nothing about
   stow at all. This is the same ruling that shaped the skill at birth
   (PROVENANCE.md: "local-only by default with off-site distribution handled
   by the user") — re-applied to the new surface without amendment.
2. *"Same goes for exclusion of some paths/elements — we can't know for sure
   what structure would other agents have and exclusion shouldn't be on by
   default, but having such option is useful not only for us, so it should
   be there."* — adopted verbatim. Per-member `--exclude` added; the ONLY
   built-in patterns remain the self-exclusion class; no structural defaults
   were added.
3. *"Proposed detections seem like nice failsafes to have."* — implemented
   as advisory warnings that never gate and never change an exit code.
4. *"Make our choice of no user acks a formal option; the option to disable
   acks shouldn't be traceless — no ack should be mentioned as much as ack,
   for honesty."* — adopted as `ack-policy`. The ruling has production
   parentage: the deployment this skill was distilled from went ackless by
   a recorded disposition in September (chat-only operator, no shell; an
   agent-typed relay ack would be self-certification borrowing the
   operator's voice), and until now that choice lived only in that
   deployment's status docs, invisible to every other user of the skill.

- **Added: per-member excludes** — `member add PATH --exclude PATTERN`
  (repeatable), stored on the member, honored while walking that member
  (fnmatch on the root-relative path and the basename, same dual-match
  discipline as the global list). Patterns of the wrong shape are refused at
  config load (the global `exclude` list, previously unvalidated, is
  shape-checked too — additive, since any working config already holds valid
  patterns).
- **Changed: excluded directories prune the walk.** Previously only the
  directory *entry* was dropped and the descent continued, so one pattern
  excluded the entry but not the files under it — the documented
  two-pattern gotcha, now closed: one pattern means the subtree. Configs
  that already listed both forms behave identically (strictly less work);
  no bundled test asserted the leaky behavior.
- **Added: `evict PATH --stow-to DIR|--stow-cmd CMD [--note NOTE]`** —
  custody-preserving member removal. Packages the member's current content
  (own excludes honored) with a per-member hash map and an
  `evict-manifest.json` into `<chain>-evict-g<HEAD>-<ts>-<name>.tar.gz` +
  receipt, hands the package to the destination, and only then untracks the
  member and appends an `event=evict` witness line (through the same
  adapter/consent path as every event). Refuses without a destination
  (silent custody loss is the failure it exists to prevent; `member remove`
  stays the deliberate silent drop), refuses non-members, and **refuses to
  untrack when the hand-off fails** — custody is established before
  tracking stops, never after. `--stow-to` hash-verifies the copy at the
  destination (the roundtrip pattern); a mismatched copy is deleted, not
  left to impersonate custody. Files on disk are never touched.
- **Added: `build --stow-to DIR / --stow-cmd CMD`** — the same hand-off for
  a finished, drill-passed archive. `--stow-to` copies archive + receipt and
  hash-roundtrips the copy; `--stow-cmd` pipes the bytes to the operator's
  own command on stdin (exit code = its claim of success; reported as
  "claimed, not verified"). Failures warn and never gate: the archive
  already exists. Successes append `event=stow` witness lines. The stow
  command is **never read from config** — the planted-config attack class
  has no surface (SECURITY.md § Custody hand-off and eviction).
- **Added: detections** — advisory `DETECT` warnings on build (stderr; never
  stdout, never gates): archive growth vs the parent generation (parent
  archive locally resolved; silently skipped when it is not — a skipped
  advisory is documented, not a fencing claim), duplicate content across
  member paths, largest members entering the chain; `status` now prints raw
  member totals and archive totals, plus the custody-op trail
  (`event=evict|stow|ack-off|ack-on`). Config `detect` object:
  `growth_pct` (50), `growth_mb` (4), `archive_mb` (32), `enabled` (true);
  shape-validated at load.
- **Added: `ack-policy [off|on] [--note NOTE]`** — the ack policy, with the
  rule that a policy change is itself witnessed. Acks are witnesses, not
  gates, so disabling them is legitimate; what it may never be is
  traceless: `off`/`on` append `event=ack-off` / `event=ack-on` through the
  same adapter path and consent boundaries as acks themselves, and both
  REFUSE without a reachable ledger (adapter `none` included) — an
  un-witnessable policy change is refused, not made, and the config is
  left untouched by the refusal. While off: `ack GEN` refuses, naming the
  recorded decision and the re-enable path; `status` shows the policy;
  `verify`'s empty-witness note attributes the absence to the policy
  ("absence is policy, not neglect") instead of reading as perpetual debt.
  Historical acks remain on record and are still shown. Config
  `ack_policy` is operational state only (shape-validated at load; mode
  `off` with string `ts`/`note` and integer `gen`); the ledger line is the
  durable record. Default (key absent) is byte-identical to prior
  behavior, and policy lines are invisible to the build-entry parser by
  the same line-start anchor as every other witness class.
- **Added: ledger `event=evict|stow|ack-off|ack-on` witness lines** —
  invisible to the build-entry parser by the same line-start anchor as
  acks/events;
  `next-gen` untouched; adapter `none` and unreachable ledgers degrade to
  the documented best-effort behavior (the eviction package manifest is the
  durable record).
- **Compatibility:** no manifest/ledger format change, no exit-code change,
  no default-behavior change; `is_excluded` gained an optional parameter;
  `ledger_state` gained an `ops` key (additive). 184 assertions from 1.1.1
  pass unchanged.

RESIDUAL_RISK standing-rule payment (three questions, per feature):

- **Per-member excludes.** New failure it introduces: *the silent hole* — a
  mistyped pattern removes paths from every future archive with no warning
  at all (the one risk class in this skill that produces no signal at build
  time). Duplicates no existing witness; it is a negative capability.
  Failure mode is silent-by-nature, so the compensating controls are human:
  `member list` displays patterns, `status` prints raw weight so missing
  weight is noticeable, wrong shapes refuse at load. Recorded as
  RESIDUAL_RISK item 8.
- **Evict + stow.** New failure: a side-bucket copy that *claims* success
  (stow-cmd exit 0) without the skill being able to check the bytes —
  custody theater one flag away. Named on the output line itself
  ("claimed, not verified"), and `--stow-to` remains the only
  hash-verified path. A failed eviction now keeps the member — the
  control's own failure mode fails loud and refused. Duplicate cost: it
  re-witnesses what the package receipt already proves, buying an
  off-workspace record of the *act* (which the receipt cannot do — it dies
  with the workspace). RESIDUAL_RISK item 9.
- **Detections.** New failure: habituation (a detector that cries wolf
  trains its reader) and false precision (raw bytes ≠ compressed weight;
  duplicate detection sees only members collected this build). Named in
  output ("advisory, never gates") and in RESIDUAL_RISK item 10; the
  never-gate rule is the mitigation for both. Duplicates the size
  information `status` always had implicitly — deliberately: the audit's
  lesson was that implicit is invisible. RESIDUAL_RISK item 10.
- **Ack policy.** New failure: *ackless legitimacy* — the only thing
  distinguishing "disabled by decision" from "nobody watching" is one
  authored, forgeable ledger line, and the record dies with the ledger (a
  wipe that takes both collapses the distinction back to reader judgment).
  Named in the annex as item 11. Compensations are placement and refusal,
  not strength: the line lives where an ack would have lived (same
  adapter, same consent boundaries), no reachable ledger means no policy
  change and a config untouched by the refusal, and read-side honesty
  comes from attribution (`status`/`verify` name the policy) rather than
  from any new gate. Duplicates no witness — it is a policy over an
  existing one; the cost is one more line class in the ledger parser, under
  the same trust model as the others. Failure mode: fails loud at change
  time (refusals); at read time it is attribution, not enforcement.

Tests: 184 → 271 (T29–T33): per-member excludes end to end + walk pruning +
shape refusals; evict refusals, stow roundtrip MATCH, custody-failure member
retention, evict-manifest contents, witness lines; build stow happy/failed
paths + default silence; detections armed/disabled/tuned + status surfaces;
ack policy: off/on witnessed, ack refusal under policy with the re-enable
path named, status/verify attribution, parser discipline (policy lines never
advance next-gen), adapter-none refusal with config untouched, corrupt
`ack_policy` refused at load.
