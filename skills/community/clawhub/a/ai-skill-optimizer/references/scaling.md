# Self-Scaling Governance Reference (micro tier)

| Field | Value |
|---|---|
| Applies to | `ai-company` skill package |
| scale_tier | `micro` |
| Version | 1.0.0 (major = tier ordinal, see Section 8) |
| Upgrade policy | `propose-only` (never auto-install) |
| State file | `.scaling-state.json` (schema_version 1) |
| Config file | `scripts/scaling-config.json` (schema_version 1) |
| Executor | `scripts/self-scale.ps1` (Windows PowerShell 5.1 compatible) |
| Max tier | `group` |

This reference is the machine-readable contract for the self-scaling mechanism.
It defines the thresholds, the upgrade path, the safety gates, and the execution
sequence that `scripts/self-scale.ps1` implements. **What is documented here is
what the script does — nothing more.**

---

## 1. Three-Stage Architecture: Propose, Approve, Install

Self-upgrading is **not** self-rewriting. The mechanism is split into three
stages with strictly separated authority:

| Stage | Actor | What happens |
|---|---|---|
| 1. Propose | The skill itself | Detect thresholds, derive the upgrade path, generate a complete upgrade package under `{WORKSPACE_ROOT}/.skill-upgrade/<timestamp>/`. `{SKILL_DIR}` is read-only throughout (the only writable file is the operational state `.scaling-state.json`). |
| 2. Approve | A human | Review the upgrade report, change list, frontmatter diff, and gate results. |
| 3. Install | An external trusted installer | Apply the package to `{SKILL_DIR}`. The skill does not participate and has no authority to participate. |

Why this is non-negotiable:

| Constraint | How the three-stage design satisfies it |
|---|---|
| The skill directory is read-only (P21) | The `permissions` block is copied verbatim; the package is written to the workspace, never to `{SKILL_DIR}`. |
| No self-escalation | The skill physically cannot write its own directory, so it cannot grant itself write access. |
| No self-exemption | The skill cannot modify `tests/**`, so acceptance criteria are immune to upgrades (see Section 6, G2). |

The accepted cost: every tier upgrade requires one human approval plus one
external installation. A tier upgrade is a breaking change (all department
slugs change, frontmatter is rebuilt, major version +1) and should never run
unattended.

### 1.1 Three things that can never be self-modified (hard boundary)

Even with human approval, in any tier, on any upgrade path, the following are
immutable (README-FOR-AI.md §9.5):

| # | Immutable item | Consequence if modified | Gate | Error code |
|---|---|---|---|---|
| 1 | The `permissions` block (including `write` scope and the 5 `deny` items) | Self-escalation: all security constraints become void | G1 / G3 | `SCL_004` |
| 2 | All files under `tests/**` | Self-exemption: acceptance loses its meaning | G2 | `SCL_005` |
| 3 | The gate logic in `scripts/self-scale.ps1` | The skill could disable its own safety gates | G3 | `SCL_004` |

Human approval is the right control for **business-scale changes** (more
departments), never for **security-boundary changes**. Security-boundary changes
require regenerating the specification and a fresh human audit — they cannot
travel through the upgrade channel.

---

## 2. Upgrade Capability Matrix

| Tier | Upgrades to | major after | File count (R3 audited values) | Notes |
|---|---|---|---|---|
| `micro` | `small` | 1 → 2 | 25 → 29 | 2 → 5 departments, function blocks stay 18; package includes `README-FOR-AI.md` (user-approved deviation), so 28 spec files + 1 |
| `small` | `medium` | 2 → 3 | 29 → 36–44 | 5 → 9 departments, shared modules added (a 35–43 file range plus the package-local `README-FOR-AI.md`) |
| `medium` | `large` | 3 → 4 | 35–43 → 147 | 9 → 18 departments, D3 layer + 7-domain routing + department-index.md |
| `large` | `group` | 4 → 5 | 147 → 245 | 18 → 36 departments, function blocks 18 → 36 (the only change of block total) |
| `group` | — | — | — | Highest tier; an upgrade request returns `SCL_009` |

Rules:

- **One tier at a time.** Cross-tier jumps (`micro` → `large`) are illegal and
  return `SCL_002`. Each split mapping is defined for adjacent tiers only; a
  cross-tier move must be executed as two serial, individually approved
  upgrades.
- **Implementation scope of this build:** the executor script implements the
  `micro` → `small` edge only. Because step 5h copies the script byte-for-byte
  (and G3 enforces that), the `small`-tier package inherits this same script;
  running it at `small` tier correctly reports `SCL_002` (no mapping defined)
  until the package is regenerated at the higher tier per the specification.
- **Governance file layer does not change shape across upgrades**: 13 files
  before and after. File-count deltas come entirely from the department layer.

---

## 3. Upgrade Trigger Thresholds (T1–T4)

All thresholds are quantified. No "when the department feels overloaded" or
"evaluate as needed" wording is permitted anywhere in this mechanism.

| # | Trigger | Quantified condition | Data source |
|---|---|---|---|
| **T1** | Agent capacity overflow | Actual agent count > tier cap (micro 3 / small 10 / medium 50 / large 200) | `.scaling-state.json` → `last_metrics.agent_count` |
| **T2** | Function-block overload | Blocks in a single department > tier mean × 1.5. Micro mean = 18 / 2 = 9.0, so the threshold is **> 13.5**: a single department with **≥ 14 blocks** overflows | Count of `^## FB-\d+:` headings in D2 pages |
| **T3** | Routing accuracy drop | `department: auto` hit rate **< 85%** on **3 consecutive evaluations** | `last_metrics.routing_accuracy` + the `routing_miss_streak` counter maintained by the script in the state file |
| **T4** | Error-code reuse excess | Share of distinct functions sharing one code under a single prefix **> 25%** | `last_metrics.error_code_reuse_ratio` (aggregated from `error-codes.md` analysis) |

Per-tier T2 thresholds (mean = 18 / department count, threshold = mean × 1.5):

| Tier | Block mean | T2 threshold | Meaning |
|---|---|---|---|
| micro | 18/2 = 9.0 | **> 13.5** | A department with ≥ 14 blocks overflows |
| small | 18/5 = 3.6 | > 5.4 | A department with ≥ 6 blocks overflows |
| medium | 18/9 = 2.0 | > 3.0 | A department with ≥ 4 blocks overflows |
| large | 18/18 = 1.0 | > 1.5 | A department with ≥ 2 blocks overflows (a large-tier department should never hold ≥ 2 blocks; hitting this means the package should be group) |
| group | 36/36 = 1.0 | n/a | Highest tier |

Micro-tier concrete values (what the script evaluates on every `evaluate` run):

- **T1**: `agent_count > 3` (cap 3 × headroom 1.0, from `scaling-config.json`)
- **T2**: `max_blocks_per_department > 13.5` (i.e. ≥ 14), counted live from the D2 pages
- **T3**: `routing_accuracy < 0.85` on 3 consecutive runs (the streak counter
  resets to 0 on any run at or above the floor)
- **T4**: `error_code_reuse_ratio > 0.25`

Trigger rules:

- Any T1–T4 hit → the skill autonomously **generates an upgrade proposal**
  (never installs it).
- T3/T4 hit while T1 is not hit → the proposal must state "capacity has not
  overflowed, but the structure no longer fits".
- No trigger hit → update `next_evaluation` (default +30 days, from
  `evaluation_interval_days`) and `last_metrics` in the state file, then exit.
- Forced invocation (`-Force`) with no threshold hit → a proposal is still
  generated, and the report's first line carries the `SCL_001` warning.

---

## 4. micro → small Upgrade Path (merge tree)

The split mapping below is a **deterministic table lookup** from the
merge tree in README-FOR-AI.md §10.1. The executor performs no AI improvisation of
department boundaries.

### 4.1 Department split (2 → 5)

| Legacy slug (micro) | Prefix | New slug (small) | Prefix | Blocks moved |
|---|---|---|---|---|
| `governance-and-delivery` | `CEO_` | `governance-and-operations` | `CEO_` | 6 |
| `governance-and-delivery` | `CEO_` | `quality-and-delivery` | `CQO_` | 2 |
| `engineering-and-safety` | `CTO_` | `technology-and-platform` | `CTO_` | 3 |
| `engineering-and-safety` | `CTO_` | `security-and-compliance` | `CISO_` | 3 |
| `engineering-and-safety` | `CTO_` | `people-and-growth` | `CHO_` | 4 |

Conservation check: 6 + 2 + 3 + 3 + 4 = **18** function blocks, unchanged
from micro's 8 + 10 = 18. The legacy slugs are retired and never reused.

### 4.2 Prefix changes

| Prefix | micro | small | Reason |
|---|---|---|---|
| `CEO_` | active (`governance-and-delivery`) | active (`governance-and-operations`) | Inherited by the successor department |
| `CTO_` | active (`engineering-and-safety`) | active (`technology-and-platform`) | Inherited by the successor department |
| `CISO_` | retired | **revived** (`security-and-compliance`) | Split revives the retired prefix |
| `CHO_` | retired | **revived** (`people-and-growth`) | Split revives the retired prefix |
| `CQO_` | retired | **revived** (`quality-and-delivery`) | Split revives the retired prefix |
| `SCL_` | active | active | Infrastructure prefix, fixed 10 codes, never changes |

### 4.3 Deterministic split rule (as implemented)

The executor splits a legacy D2 page **in page order**: the `## FB-N:` sections
are assigned to the target departments in the order listed in 4.1, taking the
block count shown in the last column. This mirrors the merge tree: the
governance/finance blocks precede the quality/delivery blocks inside
`governance-and-delivery`, and the technology, security, and people/growth
blocks appear in that order inside `engineering-and-safety`. Each new D2 file
keeps the legacy page's preamble (with the slug replaced) and its FB sections
verbatim, so no function-block content is authored or dropped by the split.
If a legacy page contains **more or fewer** `## FB-N:` sections than the
merge tree expects, the split fails immediately with `SCL_010` — leftover
sections are never silently dropped and short pages are never padded.

### 4.4 Error-code migration (step 5e)

`CEO_` and `CTO_` survive the upgrade, but some of their codes describe
functions that moved to the revived `CISO_` / `CHO_` / `CQO_` departments.
Remapping those codes requires the function-level merge lists, which are not
machine-derivable in this build. The executor therefore appends an
**error-code alias-table skeleton** to `error-codes.md` (one row per legacy
`CEO_`/`CTO_` code, every row marked "requires human review") and flags the
completion of the mappings in the upgrade report as a mandatory human-review
item; this build does not rewrite the existing code tables automatically. The
report lists the retained prefixes, the revived prefixes, and the review
requirement, and gate G6 verifies that the package's `error_code_prefixes`
frontmatter lists all five department prefixes plus `SCL_`.

---

## 5. Slug Alias Mechanism (backward compatibility)

The merge tree guarantees that **functions** are never lost, but **department
slugs all change**. A caller passing `department: governance-and-delivery`
would break immediately after the upgrade. Aliases solve this:

| Rule | Content |
|---|---|
| One-to-many is legal | A micro department splits into 2–3 small departments, so its alias naturally maps to several targets |
| Disambiguation required | When routing hits a one-to-many alias without a `domain`/`task` hint, the skill **must ask for clarification** — never guess |
| Permanent retention | Aliases are never deleted and accumulate across upgrades (a micro→large package carries micro, small, and medium generation aliases) |
| No slug reuse | A retired slug must never be assigned to a new department |
| Frontmatter pointer | After upgrade, frontmatter carries `department_aliases: references/scaling.md#alias-map` (one line) |
| Conflict detection | If a new department slug equals any historical alias → `SCL_003`, upgrade rejected |
| No translation | Aliases and slugs stay in original English form regardless of output language |

Error-code aliases work the same way: e.g. `CEO_003` (a delivery-function code
at micro tier) remaps to `CQO_001` at small tier, and `error-codes.md` keeps a
deprecated section recording the mapping (see 4.4 for what is automated).

## Alias Map

Active aliases (parsed by gate G5; table rows only, fenced examples are
ignored):

| Legacy slug | Legacy tier | Resolves to | Since |
|---|---|---|---|
| _(none — initial micro tier, no upgrade has occurred)_ | — | — | — |

Planned rows appended by the micro → small upgrade (illustrative, not active):

```text
| Legacy slug             | Legacy tier | Resolves to             | Since  |
|-------------------------|-------------|-------------------------|--------|
| governance-and-delivery | micro       | governance-and-operations | v2.0.0 |
| governance-and-delivery | micro       | quality-and-delivery     | v2.0.0 |
| engineering-and-safety  | micro       | technology-and-platform  | v2.0.0 |
| engineering-and-safety  | micro       | security-and-compliance  | v2.0.0 |
| engineering-and-safety  | micro       | people-and-growth        | v2.0.0 |
```

---

## 6. Six Upgrade Safety Gates (G1–G6)

These gates are **authority and conservation checks**, not supply-chain checks.
Each gate is an independent code branch with its own log output in the
executor; gates are never merged into a single conditional.

| # | Gate | Check (as implemented) | Failure action | Error code |
|---|---|---|---|---|
| **G1** | Permission-unchanged | SHA-256 of the `permissions` block extracted from the package `SKILL.md` frontmatter equals the SHA-256 of the current one. Zero-change; the hash is computed over normalized text (line-ending insensitive) | Reject: package quarantined | `SCL_004` |
| **G2** | Tests-unchanged | Every file under `tests/**` in the package is byte-identical (SHA-256, same relative path set) to the current package — no additions, no deletions, no modifications; equivalently, the package diff contains no `tests/**` paths. Build residues (`__pycache__/`, `*.pyc`) are excluded on both sides, so they can never fail or pad this gate | Reject: package quarantined | `SCL_005` |
| **G3** | Deny-and-gate-unchanged | The 5 `deny` items are present and unrewritten in the package, and `scripts/self-scale.ps1` in the package has the same SHA-256 as the running script | Reject: package quarantined | `SCL_004` |
| **G4** | Function-block conservation | Total `## FB-N:` headings across the package's D2 pages equals the target expectation (18 for small) **and** every department's count equals its merge-tree expectation (small tier: 6/2/3/3/4), and no unexpected D2 page exists in the package; on failure, a per-department expected-vs-found list is reported. The split itself aborts with `SCL_010` before any package is completed when a legacy page holds more or fewer sections than the merge tree expects (nothing is silently dropped or padded) | Reject: package quarantined | `SCL_010` |
| **G5** | Alias completeness | Every legacy slug has at least one alias row, every target slug is reachable, and no new slug collides with any historical alias | Reject: package quarantined | `SCL_003` |
| **G6** | Acceptance passed | Machine-checkable acceptance items on the package: file count = expected value (29 for small = 28 spec files + `README-FOR-AI.md`; excludes `UPGRADE-PROPOSAL.md` and build residues); frontmatter triple consistency (`scale_tier` / `department_count` / `function_block_count`); version agreement in the four required locations (`_meta.json`, README badge in the concrete `version-2.0.0-blue` format, `SKILL.md` frontmatter, `SKILL.md` body); `interface.department.enum` lists exactly `auto` plus the 5 small-tier department slugs (item count = department_count + 1, no retired slug); presence of all 5 target D2 files; `error_code_prefixes` lists the 5 department prefixes plus `SCL_`; `prompts/03-test-cases.md` present, `agent-invoked`, harness level ≥ L3. Full §15 acceptance including AI-content review (A–G groups, H, I, U) remains a human step recorded in the report | Reject: package quarantined with the failed-item list | `SCL_006` |

Notes:

- **G1–G3 are hard gates.** Even with human approval, a package containing
  permission, test, or gate-logic changes must not pass. Rationale: Section 1.1.
- **Rejection is recoverable, not destructive.** A failed package is moved to
  `{WORKSPACE_ROOT}/.skill-upgrade/_rejected/<timestamp>-<SCL_CODE>/` and a
  failure record is written to the state file. No `Remove-Item -Recurse -Force`
  pattern exists anywhere in the executor (P23).
- **G6 scope honesty:** the script runs the machine-checkable subset listed
  above; the report states that full §15 acceptance (including content
  quality groups) is completed by the human reviewer before approval.

---

## 7. Eight-Step Execution Sequence (as implemented)

```
1. Read .scaling-state.json
   -> confirm current_tier, last evaluation result, pending_proposals
   -> a missing, invalid, or tier-inconsistent state file stops the run (SCL_007)

2. Collect the four metrics and evaluate against the T1-T4 thresholds
   -> agent_count / max_blocks_per_department (counted live from D2 pages)
      / routing_accuracy (+ consecutive-miss streak) / error_code_reuse_ratio

3. No trigger -> write back next_evaluation (+30 days) and last_metrics,
   exit 0.
   -> if invoked with -Force, log the SCL_001 warning and continue instead

4. Triggered -> look up the split mapping from the merge tree (Section 4)
   -> deterministic table lookup; no AI improvisation of department splits
   -> current tier = group -> SCL_009; no mapping defined -> SCL_002

5. Generate the upgrade package in {WORKSPACE_ROOT}/.skill-upgrade/<timestamp>/:
   5a. new department D2 files (from the split of the legacy D2 pages) and
       the new agent-invoked prompt prompts/03-test-cases.md (S tier: 3
       prompts; its row is added to the SKILL.md Prompts index - zero orphans)
   5b. function-block split (conservation: total must equal 18 and the
       per-department distribution must equal 6/2/3/3/4; a legacy page with
       more or fewer "## FB-N:" sections than the merge tree expects aborts
       immediately with SCL_010 - nothing is silently dropped or padded)
   5c. D3 subdirectories -- not applicable for micro -> small (target < large)
   5d. new frontmatter: scale_tier / department_count / function_block_count
       updated, major version +1, department_aliases pointer added,
       interface.department.enum rewritten to auto plus the 5 new slugs, and
       the description rewritten for the small tier (5 departments, 3-10
       agents); language_policy copied unchanged; permissions block copied
       unchanged (one character of difference fails G1)
   5e. error-code migration: prefix inventory updated in frontmatter; an
       error-code alias-table skeleton (legacy code -> new code, every row
       marked "requires human review") is appended to error-codes.md; the
       actual code remapping to revived prefixes remains a human-review
       item (4.4)
   5f. department-index.md -- not applicable for target < large
   5g. slug alias rows appended to this file's Alias Map (history preserved)
   5h. the current package copied verbatim (tests/ and scripts/self-scale.ps1
       byte-identical, never modified -- this is what G2/G3 verify),
       excluding the operational state file, the retired legacy D2 pages,
       and build residues (__pycache__/ directories and *.pyc files)
   5i. governance layer: CHANGELOG.md entry inserted directly after
       [Unreleased] (Keep a Changelog order, never appended at the end);
       version strings replaced with counted, context-exact rewrites (badge,
       version table rows), every replacement location logged; the README
       Project Structure tree is rewritten to the 29-file small-tier
       skeleton and marked as requiring human review;
       LICENSE / SECURITY.md / .editorconfig / CODE_OF_CONDUCT.md /
       CONTRIBUTING.md / AGENTS.md are never touched
   5j. the package's own .scaling-state.json carries a tier_history skeleton
       entry for this upgrade (from / to / proposed_at / package_path;
       approved_by and installed_at empty; acceptance_passed false) --
       append-only, never reset to an empty array; the live state file's
       pending_proposals records the proposal (no installed_at,
       acceptance_passed false until the human §15 acceptance)

6. Run gates G1-G6 (Section 6) on the package
   -> any failure: quarantine the package, report the SCL code, write a
      failure record to the state file, exit non-zero

7. All gates passed -> generate UPGRADE-PROPOSAL.md in the package directory
   (template: proposal time, tier counts, trigger reasons, change list,
   frontmatter-diff note, gate results table, install instructions, rollback)

8. Stop.
   -> no install, no write to {SKILL_DIR} content, no permission request,
      no "upgraded" claim
   -> the proposal stays pending in the state file; approved_by / installed_at
      remain empty until a human and an external installer act
```

Step 5h is the implementation basis of gates G1/G2/G3: the copied `tests/` and
`self-scale.ps1` must be byte-identical to the current package. The generation
logic is designed never to produce changes to these files in the first place.

Step 8 wording requirement: the delivery message must state "proposal
generated, **not yet effective**, requires human approval before installation".
Saying "upgraded to small tier" is prohibited — the change has not taken effect.

---

## 8. Version Number Policy

A tier upgrade is a **breaking change** (department enumeration changes,
frontmatter is rebuilt, legacy slugs move into alias resolution), therefore:

| Change type | Version increment |
|---|---|
| Tier upgrade | **major +1**, minor/patch reset to 0 |
| Department responsibility revision (no structural change) | minor +1 |
| Typo fixes, threshold tweaks, alias additions | patch +1 |
| Downgrade | major −1, never below v1 (see Section 9) |

Tier-to-major mapping — **the major version number equals the tier ordinal**,
double-confirming `scale_tier`:

```
micro   v1.x.x
small   v2.x.x   <- from a micro upgrade
medium  v3.x.x
large   v4.x.x
group   v5.x.x
```

Four version locations must always carry the **same value** (acceptance H15):
`_meta.json`, the README badge, the `SKILL.md` frontmatter, and the `SKILL.md`
body title. The micro → small upgrade bumps all four from `1.0.0` to `2.0.0`,
and gate G6 verifies the agreement.

---

## 9. Downgrade Policy (shrinking scale)

Downgrading is **more dangerous than upgrading**: an upgrade only adds files
(legacy content survives in aliases and function blocks), while a downgrade
deletes files and merges content — a bad merge permanently destroys
specification detail.

| Item | Rule |
|---|---|
| Automatic downgrade | **Never allowed.** Downgrading is a lossy operation |
| Human trigger | Explicit approval **plus a written rationale**, recorded in `tier_history` |
| Error code | `SCL_008` (downgrade requires human approval) |
| Tier span | Same as upgrade: one tier at a time |
| Function blocks | Conservation inverted: group → large merges 36 → 18 (the only operation allowed to change the block total) |
| Error codes | Never a plain merge: many-prefix → one-prefix requires remapping; legacy codes stay as deprecated aliases |
| Slugs | All legacy slugs stay as aliases pointing at the merged departments (many-to-one, the reverse of upgrade) |
| D3/D4 layers | large → medium deletes 18 D3 subdirectories and 4 cluster subdirectories; group → large deletes the D4 engine layer; deletion is only allowed after confirming the content was merged into D2 |
| Governance layer | No file is ever deleted; only `CHANGELOG.md` and `README*.md` structure trees are updated |
| Version | major −1, floor v1 |
| Executor | Same as upgrade: the skill only generates a downgrade proposal package; installation is external |

Implementation status in this build: **downgrade is outside the capability of
the executor script.** The script's `param` block has no `downgrade` action
value, and no code path can generate or handle a downgrade. A downgrade
follows the manual process of README-FOR-AI.md §12.5 (human approval with
a written rationale, executed by an external installer); where `SCL_008`
semantics apply, they are carried by the external installer, not by this
script. A downgrade proposal report must additionally contain a
**destination table for all deleted content** — every
section of every deleted file must name the D2 function block it was merged
into. Deletion must go through the recycle bin or a backup, never
`Remove-Item -Recurse -Force` (P23).

---

## 10. SCL_ Error Codes

| Code | Meaning |
|---|---|
| `SCL_001` | Forced proposal generated although no threshold was hit (warning) |
| `SCL_002` | Illegal upgrade mapping: cross-tier jump requested, or no mapping defined for the current tier |
| `SCL_003` | Slug/alias conflict: a new slug collides with a historical alias, or alias coverage is incomplete |
| `SCL_004` | Permissions block or gate-logic file was modified (G1 / G3) |
| `SCL_005` | tests/** was modified (G2) |
| `SCL_006` | Upgrade package failed acceptance checks (G6) |
| `SCL_007` | State file missing, invalid, or inconsistent with frontmatter |
| `SCL_008` | Downgrade requested — requires human approval (not implemented; manual process) |
| `SCL_009` | Already at the highest tier (group); no upgrade path exists |
| `SCL_010` | Function-block conservation failed (G4) |

---

## 11. Usage

All commands use placeholders; never hardcode absolute user paths (P18):

```powershell
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action evaluate
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action evaluate -DryRun
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action evaluate -Force
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action propose
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action status
pwsh -File "{SKILL_DIR}/scripts/self-scale.ps1" -Action report
```

| Action | Effect |
|---|---|
| `evaluate` | Full 8-step sequence: read state, collect metrics, evaluate T1–T4; generate a proposal only if triggered (or `-Force`) |
| `propose` | Generate a proposal package directly (marks `SCL_001` in the report if no threshold was hit) |
| `report` | Print the upgrade report of the latest pending proposal |
| `status` | Print tier, metrics, thresholds, and pending proposals |

There is deliberately **no** `install`, `apply`, or `commit` action (P36).
Exit codes: `0` = success / no trigger; `2` = fatal `SCL_` stop; `3` = gate
failure (package quarantined).

### 11.1 External installer requirements (recorded in every proposal report)

```
The installer must: Copy-Item to a temporary directory -> verify integrity ->
atomically replace -> only delete the old directory after confirming success.
Forbidden: Remove-Item -Path {SKILL_DIR} -Recurse -Force followed by a
restore (P23). Backup directories must be cross-platform: fall back from
$env:USERPROFILE to $HOME when the former is empty (P26).
```
