# Verification Record

This file is the verifiable material behind SKILL.en.md's smoke-test claim ("smoke-tested on a real Jira with three-level dedup and change correlation"). Anyone can re-run it in minutes using "How to re-run" at the end.

## Environment

- Date: 2026-11-13
- Tracker: a real Jira instance (read-only credentials, queried via the platform's MCP tool; ticket IDs redacted here)
- Code repository: a real local git repository
- Method: executed step by step per SKILL.en.md, fully read-only

## Scenarios and Results

### Scenario 1: dedup hit (main path)

- Input: a real backend defect description (exception type and error code included)
- Execution: normalized fingerprint → level-1 full-fingerprint search → hit
- Result: hit one open ticket (ID redacted), similarity graded "high" — all fingerprint-present core items matched; output included the evidence chain and a ticket-filing suggestion; zero write operations
- Pass criteria: ✓ hit, with the similarity grade consistent with the FAQ baseline

### Scenario 2: no match (honest degradation)

- Input: a brand-new frontend style defect (the reachable tracker does not cover that domain)
- Execution: all three ladder levels executed
- Result: no hits at any level, verdict "no", with the honest note "the reachable tracker does not cover this domain" — nothing fabricated
- Pass criteria: ✓ Iron Law 1 (no "known" without a search) and honest degradation hold

### Scenario 3: change correlation (git blame)

- Input: a backend defect with the involved layer known
- Execution: read-only `git log` / `git blame` over recent merges and authors of the failing area
- Result: listed recent changes and authors as ownership-inference evidence; the pure-frontend case correctly skipped step 3
- Pass criteria: ✓ Iron Law 2 (no ownership claim without evidence) holds

## How to Re-run

1. In an environment with a tracker query tool configured, say "triage this bug" and paste a defect description from a known ticket → it should hit that ticket (verifies dedup)
2. Paste a brand-new issue → it should report "no" after the full ladder (verifies honest degradation)
3. Ask ownership for a backend defect → the output should include the git evidence chain (verifies ownership inference)

Every step is read-only; no re-run should produce tracker write operations.
