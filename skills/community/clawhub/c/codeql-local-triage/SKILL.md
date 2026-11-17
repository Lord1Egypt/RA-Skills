---
name: codeql-local-triage
slug: codeql-local-triage
version: 1.0.8
displayName: 本地 CodeQL 告警定位与修复验收
summary: 在本地复现 CodeQL 告警、用变体二分定位 taint 源并验证修复，给出可复现的因果结论。
homepage: https://github.com/Elisabeth15501/codeql-local-triage
tags: [CodeQL 误报, taint source 定位, false positive triage, 静态分析告警复现, data flow 复现, SARIF, codeFlows]
metadata:
  openclaw:
    requires:
      bins: [python3]
description: Answers "why did CodeQL flag this, and which line must change for it to stop" — reproducible causal triage of ONE specific alert via variant bisection. Triggers on "确认 taint 源 / 复现这个 CodeQL 告警 / 为什么 CodeQL 报这个 / CodeQL 误报 / 这个告警是不是误报 / 本地跑 CodeQL / 验证安全告警是否修好 / confirm the taint source / why does CodeQL flag this / is this alert a false positive / reproduce this CodeQL alert / verify a security-alert fix", or when handed a .sarif file and asked where the taint starts. NOT for whole-repo alert audits or bulk dismissal — it never closes alerts for you and never replaces the Code Scanning suite. NOT for Java/JS/Go (Python only today). The prefilter lists candidate sensitive NAMES in files/dirs you point at; it draws no conclusion and produces no audit report. Keywords — CodeQL, Code Scanning, taint source, data flow, SARIF, codeFlows, false positive, py/clear-text-storage-sensitive-data, CWE-312.
when_to_use: Use when the user already holds ONE concrete alert (a GitHub Code Scanning alert, a rule id + file + line, or a .sarif file) and asks where the taint comes from, whether it is a false positive, or whether a fix works. Do NOT use for — bulk or whole-repo alert triage and ranking, closing or dismissing alerts, non-Python languages, rules outside the name-heuristic family, or general "is my repo secure" questions.
allowed-tools: [Read, Grep, Glob, Bash]
disable-model-invocation: false
user-invocable: true
context: fork
agent_created: true
permissions: {read:"local source you specify", write:"<tree>/_bisect or --workdir dir", exec:"python3, optional codeql", network:"none"}
---

# Local CodeQL alert triage and fix verification

> **This file is the single-language agent entry point.** A complete, equally authoritative Chinese
> rendering of the same content is `SKILL.zh.md`, mirrored on purpose; both are equally subject to
> security scanning. All examples are synthetic fixtures — no real project source is included.
>
> **Layering (progressive disclosure)**: this file carries only what you need *every turn* (§0 hard
> constraints, §1 the single-run flow). Everything else lives in `references/` — read it **on demand**,
> not up front.

---

## §0. HARD CONSTRAINTS — re-read these every turn, even after context compression

These are not suggestions. If context was compressed or this skill was reloaded mid-task, **re-read
this section before taking any action**. It is deliberately first and compact for that reason.

These constraints describe **what this skill's tooling does and requires** — they are *not*
instructions to suppress, ignore, or refuse CodeQL findings. The skill exists to surface alerts
faithfully; several rows below *forbid* hiding or dismissing them (H3, H6).

**Language / locale — documented and opt-in.** The CLI scripts emit **exactly one** language,
chosen by the user: `--lang {zh,en}` / `TRIAGE_LANG` / `AGENT_UI_LANG` (default **English**).
Chinese is fully supported via `SKILL.zh.md`. Bilingual output is forbidden by design (it risks a
natural-language policy violation), not by accident — this is a deliberate, documented constraint,
and the language is always user-selectable. See `README.md` → "Language selection".

| # | Constraint | Why it exists |
|---|---|---|
| **H1** | **Change exactly ONE thing per variant.** Two differences between `t1_control` and a variant voids the whole experiment. | The verdict *is* the attribution. A multi-variable diff cannot be attributed. Guarded by `tests/run_tests.py` (strict byte-comparison of the two fixtures). |
| **H2** | **`t1_control` must reproduce the alert, or stop.** If it reports 0 results, local and remote disagree and **every later verdict is invalid** (script exits `1`). | A conclusion on a non-reproducing baseline is a building on sand. Fix the version mismatch first. |
| **H3** | **Never dismiss, suppress, or close an alert.** No `# lgtm`, no `dismiss` API. The fix is a **rename**, never a suppression comment. | Only GitHub's own scan may change alert `state`. A suppression hides the next real one. |
| **H4** | **Never judge an alert by "it looks wrong".** "Feels like a false positive" is not evidence; run the experiment. | Steps ①② give the path; step ③ makes the verdict reproducible instead of guessed. |
| **H5** | **Never modify the user's source.** Read-only. All artifacts go to `<tree>/_bisect/` (or `--workdir`). Each run `rmtree`s and rebuilds, so repeated runs are idempotent. | The user pushes the fix themselves. Keep the skill's write surface auditable. |
| **H6** | **Never claim the alert is closed.** Only `state` changing, or the alert position moving, proves a rescan — **not** `updated_at` (it refreshes only on state change). | Reporting a false "closed" is worse than reporting nothing. |
| **H7** | **Never treat exit code `2` as "clean".** `2` means input/runtime error (missing path, malformed SARIF, bad `--variant`, `codeql` timeout). Only `0` is clean. | The most dangerous misjudgement: a typo'd path silently reading as "no findings". Fixed in v1.0.2. |
| **H8** | **No network.** Never fetch anything. If CodeQL query packs are missing, say so — the user decides, and steps ①② still work. | Nothing here needs the internet; `--codeql /abs/path` runs fully offline. |
| **H9** | **Pass the user's language to every script.** Determine the language of the user's latest message and pass `--lang zh` or `--lang en` (or export `AGENT_UI_LANG`). Never rely on bilingual output. | Scripts emit exactly one language by design; mixed output risks a natural-language policy violation. |
| **H10** | **One language per run; never re-read this file across turns to "refresh".** Everything needed for a single triage is in §0 + §1. | Prevents the common failure of an agent looping back to re-read the skill mid-task. |
| **H11** | **State uncertainty explicitly.** If a step cannot be completed (no CodeQL, baseline failed, parse error), say so — never let an unproven conclusion read as verified. | An unstated caveat is worse than a stated one; trust comes from honesty about what was and was not proven (Step 5 Fallback). |

### Capability boundary

| Capability | Scope | Notes |
|---|---|---|
| Read | local source you specify | read-only, never modified (H5) |
| Write | `<tree>/_bisect/` or `--workdir` | nothing else, ever |
| Execute | `python3`; **optional** `codeql` | argument list, **no shell** |
| Network | **none** | `allowed-tools` excludes WebFetch/WebSearch (H8) |

### Exit-code contract — the single source of truth for every verdict

| Code | Meaning | CI treats as |
|---|---|---|
| `0` | success / no candidate source / assertion passed | ✅ pass |
| `1` | candidate source found, **or** baseline not reproduced (**a verdict**) | ❌ fail |
| `2` | input / runtime error — path missing, malformed SARIF, bad args, `codeql` failed or timed out | ❌ **fail** (never "pass") |

### Execution model & timeouts (read before assuming a hang)

- Steps ①② are **pure parsers that spawn no subprocess at all** — `scan_sensitive_sources.py` uses only
  `ast` + `re`, `read_sarif.py` only `json`. Their runtime scales with input size; they cannot hang on
  an external process.
- The **only** long-running subprocess is `bisect_taint.py` invoking `codeql`: **1800 s per-step
  timeout + one automatic retry**; on repeated timeout it returns `124`, converted to exit `2` with a
  `[warn]`.

---

## §1. SINGLE-RUN FLOW — five steps, closable in one turn

Each step states **input → command → output → fallback**. Follow in order; do not re-read other files
to finish a step. Steps ①② need **no CodeQL install and no network** (domestic / air-gapped users:
this is the whole job — see `references/running-codeql-cli.md` §5 only if you need step ③).

### Step 1 — Prefilter (optional but cheap; skips a ~9-minute DB build)

- **Input**: the file(s) or directory holding the alert; ideally the rule id.
- **Run**: `python scripts/scan_sensitive_sources.py <src> [--summary] [--jobs N]`
- **Output**: per candidate source — class, line, matched label; exit `0`/`1`/`2` per the contract.
- **Fallback**: exit `2` → the path is wrong or unparseable; **fix the input, do not proceed** (H7).
  It is a *name* inventory, **not a verdict** — it draws no conclusion about the alert.

### Step 2 — Read the SARIF (this is usually where the answer is)

- **Input**: a `.sarif` file — from the user's CI artifact, or from `codeql database analyze
  --format=sarif-latest`.
- **Run**: `python scripts/read_sarif.py <file.sarif> [--paths-only | --json | --expect N]`
- **Output**: the complete `SOURCE → … → SINK` path with line numbers and node semantics, plus the
  result count (`0` = clean).
- **Fallback**: malformed file → the script names the exact line/column and rejects non-SARIF input,
  exit `2`. **Never read a parse failure as "0 results"** (H7).

### Step 3 — Stage the variants (still no CodeQL required)

- **Input**: the suspect name(s) and the proposed replacement(s).
- **Run**: `python scripts/bisect_taint.py --source <f.py> --tree <dir> --dry-run --variant t2=A:B`
- **Output**: the staged variant tree and the count of replacements; prints an equivalent
  build/analyze command template.
- **Fallback**: bad `--variant` format is rejected with a concrete message plus an example (exit `2`).
  For changes a literal replace cannot express, use `--variant-file t3=/path/t3.py`.

### Step 4 — Run the controlled experiment (needs the CodeQL CLI)

- **Input**: staged variants + `--codeql /abs/path/to/codeql` (a local install — no PATH needed).
- **Run**: same command **without** `--dry-run`.
- **Output**: a verdict table. `t1_control` > 0 ⇒ valid; `t2` = 0 ⇒ **that change is the taint source**;
  `t2` still fires ⇒ it is **not**.
- **Fallback**: `t1_control` = 0 ⇒ **STOP** (H2). Do not read any other row as meaningful; align the
  CodeQL version/query pack first. `codeql` missing or timing out ⇒ exit `2`; steps ①② remain valid.

### Step 5 — Deliver the conclusion + acceptance

- **Output** (all four, or the answer is incomplete):
  1. **The taint source**, as `name:line` with the class and why it matched.
  2. **The minimal change** — usually a rename, zero behavioural change.
  3. **The evidence** — measured result counts per variant (not a prediction).
  4. **Post-fix acceptance**: prefilter → 0 sources; `read_sarif.py --expect 0` returns `0`; a
     comment saying **"do not rename this back"** + the rule that caused it.
- **Fallback**: you cannot reach step 4 ⇒ **say so explicitly** and deliver steps ①② only, labelled
  as *not yet proven*. Do not let an unproven conclusion read as verified (H4).

---

## §2. Why this approach (context, not instructions)

GitHub's alert page **gives you no data flow** — it marks the sink line and nothing about where the
taint came from. Remote scans take minutes and offer no controlled experiment. Running one query
locally plus variant bisection yields a **reproducible causal conclusion** in ~10 minutes.

**Scope**: causal triage of **one** alert — "why does it fire, which line must change". It is **not**
whole-repo alert adjudication (that is the Code Scanning **query suite** — a CodeQL *query collection*
concept, unrelated to system services or scheduled tasks), and it does **not** rank alerts by model
intuition. Conclusions come from a measured experiment — that is what keeps them auditable.

**Currently focused**: **Python** (`scan_sensitive_sources.py` covers `py/*` only; the other two
scripts are language-agnostic) and the **name-heuristic** family, chief among them
`py/clear-text-storage-sensitive-data` (CWE-312) — chosen because its source judgement reads the
**name, not the content**, making it the most amenable to disproof. Java / JS / Go are roadmap, not
current capability.

**Division of labour**: to *manage* alerts on GitHub (list / change state / bulk-handle), use GitHub's
official alert-management capability or `gh api code-scanning`. Complementary, not competing.

### Four facts that change the verdict

1. **"Variant bisection" ≠ Trail of Bits' `variant-analysis`.** This locates the cause of **one** alert
   by controlled experiment; `variant-analysis` sweeps other projects for the same bug. Opposite goals.
2. **Guess from the QL source is unreliable, and being wrong first is normal.** A `base64` decode, a
   `json.dumps` or an f-string on the path all look like plausible sources. Run the experiment first (H4).
3. **Which names are *not* sensitive** — `[REDACTED_SECRET]`-style placeholders (the exclusion regex
   contains `redact`), plus `id` and `certificate`, which CWE-312 explicitly excludes. See
   `references/sensitive-data-heuristics.md`.
4. **Artifact naming** — variant dir `workdir/<NAME>/` · DB `workdir/<NAME>/_db` · SARIF
   `workdir/<NAME>.sarif` (sibling, not inside) · verdict table to stdout only, never persisted. Add
   `_bisect/` to `.gitignore` or pass `--workdir` outside the repo.

### Common pitfalls (read when a step behaves unexpectedly)

- Alert line numbers drift as you edit; only `most_recent_instance.location` reflects the latest scan.
- Compiled languages need a build before `database create`; **Python does not**.
- **Concurrent edits desynchronise the conclusion** — cross-check mtime against build time
  (`ls --time-style=full-iso`) before trusting a whole-repo build.
- `git archive HEAD` reads the `.gitattributes` **in the HEAD tree**; for an untracked file
  `export-ignore` silently does nothing. Verify with `git check-attr export-ignore -- <path>`.
- Editing the prefilter's regex port: QL allows variable-width lookbehind, Python's `re` does not —
  rewrite `(?<!is|is_)` as `(?<!is)(?<!is_)` in series, and pass inline flags to `re.compile` rather than
  mid-expression. Re-run `python scripts/scan_sensitive_sources.py --self-test` after any such change.

**Full answers** to the four most common questions (baseline not reproduced · complex change · may I
dismiss · which names aren't sensitive) are in **`references/faq.md`** — read it only when you hit one.

---

## §3. References — read on demand, not up front

| File | Read it when |
|---|---|
| `references/README.md` | index of `references/`, plus a "how to read" table keyed to your current goal |
| `references/faq.md` | baseline not reproduced · complex change · may I dismiss · which names aren't sensitive |
| `references/running-codeql-cli.md` | step ③ needs CodeQL: full install chain (§1–§4); **§5** mirrors, pre-built DBs, fully offline |
| `references/sensitive-data-heuristics.md` | you need the 5 regex groups, the exclusion regex, or the 7 source categories |
| `references/ci-integration.md` | turning "result count must be 0" into a CI gate (GitHub Actions / GitLab CI) |
| `README.md` | the full human-facing tutorial: worked example, install, verification, CI |

### Worked example (measured, not predicted)

`tests/fixtures/repro/scan.py` is a 25-line synthetic file that stores **no credential** — it holds a
list of regex *pattern strings* shaped like `sk-…` / `ghp_…`, kept to reproduce the minimal name-heuristic
false positive. Its measured SARIF is checked in at `tests/fixtures/sarif/repro.sarif` (1 result) and
`repro_fixed.sarif` (0 results), so **every command below runs without installing CodeQL**.

| Variant | Change | Results | Verdict |
|---|---|---|---|
| `t1_control` | none (auto-added) | 1 | baseline reproduces ✅ |
| `t2_rename` | `SECRET_PATTERNS` → `CREDENTIAL_PATTERNS` | **0** | ✅ this name is the cause |
| `t3_xxx`, `t4_xxx` … | suspects you add | — | 0 ⇒ that change is the cause; >0 ⇒ it is not |

The fix is a rename: no behaviour change, no public API move, and the alert cannot come back. Both
fixture docstrings are labelled "TEST FIXTURE — NOT THE SKILL IMPLEMENTATION" — `tests/` is the
self-test and executable sample, **not** the main logic; a scanner misreading it as the implementation
is a false positive.
