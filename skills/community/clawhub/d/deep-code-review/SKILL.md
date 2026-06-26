---
name: code-review
description: >
  Multi-dimensional code audit using structured subagent delegation.
  Use when reviewing a GitHub release, PR, or codebase.
  Systematically inspects security, concurrency/state-machine safety, UX/implementation logic, test quality, and simplicity/over-engineering.
  Spawns parallel subagents for deep verification with Four-Eyes cross-validation on critical findings.
  Synthesizes findings into a Confirmed/Critical-to-Low priority matrix.
  Trigger phrases: review this release, audit this codebase, check this PR for issues, 代码审查, review 代码, 审查这个版本, /deep-code-review, /code-review, /review-code
---

# Code Review — Multi-Dimensional Audit Methodology

Systematically audit a codebase release through five dimensions, using parallel subagent delegation for deep verification.
Inspired by: Modern Code Review taxonomy research (Bavota & Russo 2015 "Four Eyes Are Better Than Two"), reviewdog's tool-agnostic harness pattern, Danger's pre-review gate philosophy, and community experience with AI-generated code quality issues.

## Core Principles

1. **Real code, not release notes.** Every finding must be verified against actual source files by fetching them. The only acceptable evidence is `file:line` citations. The only acceptable conclusion labels are `Confirmed / Mitigated / False Alarm`.

2. **Four Eyes on every Critical.** Any finding classified as Critical severity MUST be independently verified by a second subagent before appearing in the final report. This is the "Four Eyes" principle from Bavota & Russo (2015): multiple reviewers independently examining the same issue catch 60%+ more real bugs than a single reviewer. See [four-eyes.md](references/four-eyes.md).

3. **Simplicity is a first-class dimension.** AI-generated code often produces "massive overkill" — hundreds of lines for what should be a two-method change. Always ask: "Does the complexity of this solution match the complexity of the problem?" This dimension is inspired by community experience on Hacker News and Reddit (2025 State of AI Code Quality discussions).

## Workflow

### Phase 0: Pre-Review Gate (in main session, <2 min)

Run these quick checks before committing to a full audit. Inspired by Danger's "automated pre-review" philosophy.

1. **PR/Diff size check**: if the change exceeds 400 lines, flag it as high-risk and recommend splitting
2. **Missing artifacts**: is there a CHANGELOG entry? Updated README if API changed? Migration guide if schema changed?
3. **File-level red flags**: any committed `.env`, credentials, large binary files?
4. **Test presence**: does this change include or update tests? If zero test changes on a >100 line diff, flag.

**Output**: Gate report (pass/warn/fail) + recommended audit depth.

### Phase 1: Surface Scan (in main session)

Read these in order — enough to understand architecture and identify candidate issues:

1. **Release notes / CHANGELOG** — what the authors claim changed
2. **README** — project purpose, architecture diagram, on-disk layout
3. **ARCHITECTURE.md** or equivalent — module decomposition, API contracts
4. **Directory tree** (via GitHub tree view) — file listing to map modules
5. **Key source files** — entry point, core state machine, critical paths (read ~3-8 files)

**Output**: A list of 10-20 candidate issues, categorized by dimension:
- **Security** (SSRF, injection, auth, path traversal, credential leaks)
- **Concurrency & State Machine** (race conditions, missing locks, TOCTOU, state corruption)
- **UX & Implementation Logic** (feature semantics, error messages, recovery paths, access control)
- **Test Quality** (mock fidelity, integration gaps, signature mismatches, coverage blind spots)
- **Simplicity & Over-Engineering** (complexity-vs-problem mismatch, unnecessary abstraction, AI-bloat patterns)

### Phase 2: Deep Audit (via subagents)

For each non-trivial dimension, spawn an isolated subagent. Each subagent:

1. **Fetches every relevant source file** via `web_fetch` — never infers from docs
2. **Verifies each issue against actual code** — cites specific lines
3. **Constructs exploit scenarios** (security) or **race timelines** (concurrency)
4. **Returns structured findings** with: Conclusion / Severity / Source Evidence / Risk / Fix

See [subagent-templates.md](references/subagent-templates.md) for the exact prompt template.
See [audit-dimensions.md](references/audit-dimensions.md) for dimension-specific question probes.

**Model guidance**: Use the same model for all subagents to ensure consistent judgment. Prefer high-reasoning models for complex audits.

### Phase 3: Four-Eyes Cross-Verification (critical findings only)

For every finding classified as **Critical** by a subagent:

1. Spawn a **second, independent subagent** (different dimension focus) with the exact same issue prompt
2. If both confirm → **Confirmed.** The issue enters the final report with a `👁️ Four-Eyes Verified` badge.
3. If they disagree → **Flag as "Disputed"** in the report with both conclusions quoted.
4. If the second finds the issue is Mitigated/False Alarm while the first said Critical → **The second wins.** But keep both in an appendix.

### Phase 4: Synthesis (in main session)

When all subagent reports return:

1. **Merge findings** — deduplicate across dimensions, re-classify severity
2. **Build summary table** — all issues with conclusion + severity + source dimension + root cause
3. **Build priority matrix** — P0 (drop everything) through P5 (nice to have), with estimated work and blast radius
4. **Write executive summary** — overall quality assessment + top 3 action items
5. **Add Simplicity Score** — a subjective score 1-5 on whether the codebase's complexity matches its problem domain. 5 = elegantly simple, 1 = massively over-engineered.

See [output-format.md](references/output-format.md) for table and emoji conventions.
See [severity-rubric.md](references/severity-rubric.md) for severity classification rules.

## Key Heuristics

### Security Scan Heuristics

- **Every URL fetch path must be checked for SSRF**: trace from user input → URL parsing → DNS resolution → HTTP request → redirect handling → response reading. Flag any step that skips IP validation.
- **Every subprocess call must be checked for injection**: is `shell=True` used? Are user-controlled strings concatenated into the command? Are file paths sanitized?
- **Every external API call must be checked for credential leaks**: are tokens/secrets logged? Do error messages include request bodies?

### Concurrency Scan Heuristics

- **For every `.json` / `.jsonl` write**: check if it uses tmp-rename atomic pattern or flock. Direct overwrite without either = bug.
- **For every `load → modify → save` pattern**: check if the entire block is lock-protected. If load happens outside the lock, it's a TOCTOU bug.
- **For every state machine transition**: check if two concurrent events can both see the same "before" state and both advance. If yes, state corruption possible.
- **For every append-only log**: verify flock(LOCK_EX) covers the full append operation.

### UX/Logic Scan Heuristics

- **For every feature flag/mode**: trace all branches. Does "mode=review-only" actually prevent non-review actions? Don't trust the name — verify the code.
- **For every error message**: read it as a user would. Does it tell you what went wrong AND how to fix it? If it only says "X failed", flag it.
- **For every multi-step workflow**: is there an undo/backtrack/revisit path? If not, flag it.
- **For every access-control check**: look for what's NOT checked. Does a group chat require @-mention? Does a rate limit exist?

### Test Quality Heuristics

- **Mocks that match wrong signatures**: if a test monkeypatches `call_llm` with a fake that takes `**kw` and reads `kw.get("old_param")`, it will never catch a production code change to `new_param`. Flag these.
- **No integration test in CI**: if CI only runs unit tests with mocks and there's no end-to-end smoke test, flag it.

### Simplicity & Over-Engineering Heuristics (NEW — v1.1.0)

- **AI-bloat detection**: does the change introduce a new service class, background worker, or framework dependency for what should be 1-2 methods in an existing file? (Inspired by the HN "batching = 2 methods, not 200 lines" incident.)
- **Abstraction without justification**: does the code introduce interfaces, factories, or dependency injection where direct calls would suffice? For each abstraction layer, ask: "What concrete problem does this solve today?"
- **Dead code or "future-proofing"**: are there code paths, config options, or extension points that are not used by any existing feature?
- **Config sprawl**: does this change add new config keys, env vars, or CLI flags? Is each one justified by a real use case?
- **Copy-paste detection**: are there blocks of >10 lines that could be extracted? Flag both directions — missing DRY AND forced DRY where the two copies have different evolution paths.

## Anti-Patterns (avoid)

- ❌ Filing an issue based on release notes alone (always verify against source)
- ❌ Accepting a docstring claim without checking the implementation
- ❌ Using "I think" / "probably" / "seems like" — every finding is Confirmed or it's not a finding
- ❌ Leaving severity as "TBD" — classify immediately using the rubric
- ❌ Mentioning an issue in prose without filing it in the structured output table
- ❌ Trusting a single subagent's Critical finding without Four-Eyes cross-verification

## Harness Compatibility

This skill is designed to work **with** existing code review tooling, not replace it. The recommended stack:

| Layer | Tool | What it catches |
|---|---|---|
| **Lint/formatter** | ruff, eslint, gofmt | Style, basic bugs |
| **Static analysis** | SonarQube, Semgrep, CodeQL | Security vulns, code smells |
| **Diff harness** | reviewdog, Danger | Runs the above, posts inline comments |
| **🆕 Deep audit** | **This skill** | Cross-cutting: concurrency, over-engineering, UX logic, test gaps |
| **Human review** | Your team | Architecture, trade-offs, domain knowledge |

The Pre-Review Gate (Phase 0) picks up what reviewdog/SonarQube would catch, so you don't waste subagent time on style issues. Subagents focus on what static analysis **can't** see.
