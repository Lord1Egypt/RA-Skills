---
name: clawcheck
description: Two-phase audit: fast deterministic scan + LLM deep quality review for security, cron, config, and skills
metadata: {"openclaw":{"emoji":"🩺","requires":{"bins":["python3"]}}}
user-invocable: true
---

# ClawCheck

Two-phase audit: a fast deterministic scan catches structural issues, then you (the agent) do a deep quality evaluation on the flagged areas.

## When to Use

- After initial setup or major config changes
- Before publishing skills to ClawHub (quality gate)
- Periodic health check (weekly cron or manual)
- When something feels off but `openclaw doctor` says "ok"
- After installing new skills or updating OpenClaw

## What This Checks vs Built-in

| This skill | `openclaw doctor` (built-in) |
|---|---|
| Secrets exposure + token hygiene | Config JSON schema validation |
| Cron ops health + prompt quality review | Plugin/skill eligibility |
| Config optimization + value assessment | Channel connectivity |
| Skill structural + content quality audit | State migrations, browser detection |

## How It Works: Two Phases

### Phase 1: Deterministic Scan (fast, free)

Run the script to get a structural baseline:

```bash
python3 {baseDir}/scripts/audit.py
```

Individual modules:
```bash
python3 {baseDir}/scripts/audit.py --security
python3 {baseDir}/scripts/audit.py --cron
python3 {baseDir}/scripts/audit.py --config
python3 {baseDir}/scripts/audit.py --skills
```

This produces JSON with scores, findings, and the bottom/top skill lists. Use this as your triage map for Phase 2.

### Phase 2: Deep Quality Audit (you, the agent)

After running the script, perform these evaluations. Budget your depth based on what the user asked for ("quick check" = Phase 1 only, "full audit" or "quality review" = both phases).

#### 2a. Config Quality Review

Read `~/.openclaw/openclaw.json` and evaluate:

- **Heartbeat prompt**: Read `agents.defaults.heartbeat.prompt`. Is it specific enough to catch real issues? Does it avoid heavy operations? A good heartbeat prompt is < 200 words, checks 2-3 things, and has clear escalation criteria.
- **Model choices**: Is the primary model appropriate for the workload? Are fallbacks a meaningful step-down (not the same tier)? Is the subagent model cheaper than primary?
- **Compaction thresholds**: Are `reserveTokens` and `keepRecentTokens` reasonable for the context window size? Rule of thumb: reserve should be 15-20% of contextTokens.
- **Session maintenance**: Are `pruneAfter`, `maxEntries`, `rotateBytes` set to values that match the usage pattern? Heavy cron usage needs more aggressive pruning.
- **Cron maxConcurrentRuns**: Is it high enough for the number of frequent jobs? Count jobs with `*/` in their schedule expression.

Score each aspect 1-5. Report specific improvements.

#### 2b. Cron Prompt Quality Review

Read `~/.openclaw/cron/jobs.json`. Select the 5 most important enabled jobs using this heuristic:
1. Any job in error state (from Phase 1 findings)
2. Jobs with highest `frequency x timeoutSeconds` (most resource-consuming)
3. Jobs running on expensive models (opus/primary)
4. If still under 5, pick by business impact (backups, monitoring, user-facing)

For each selected job evaluate:

- **Prompt clarity**: Specific enough to execute without guessing? Clear steps, expected output format, error handling?
- **Safety**: Has guardrails? ("NEVER run git push", "read-only", "do not edit files directly")
- **Efficiency**: Token-efficient? Flag prompts > 1500 chars that run on expensive models. Could the prompt reference a skill file instead of inlining instructions?
- **Output value**: Produces actionable output or just noise?
- **Timeout**: `payload.timeoutSeconds` set and reasonable for scope?

Score each job 1-5 on: purpose, prompt quality, safety, efficiency. Flag jobs scoring below 3.

**Cross-reference**: Check if any cron prompts reference skills that scored below 70 in Phase 1. A cron job is only as reliable as the skills it depends on.

#### 2c. Skill Content Quality Review

From the Phase 1 results, pick:
- The 3 lowest-scoring skills (from `bottom_5`)
- Any skills the user specifically asks about
- Skills used by failing cron jobs (cross-reference cron findings)

For each selected skill, read its full SKILL.md and evaluate:

- **Accuracy** (2x weight): Would following these instructions produce correct behavior? Are API references current? Are file paths real?
- **Completeness** (1.5x): Are all use cases covered? Edge cases? What happens when dependencies are missing?
- **Clarity** (1x): Can an agent follow this without ambiguity? No hedging, clear steps, good examples?
- **Efficiency** (1x): Is the SKILL.md bloated? Could it be shorter without losing information? Does it suggest efficient patterns (batching, caching)?
- **Voice alignment** (1x, content-producing skills only): Does the output match the brand/user's tone?

Scoring formula depends on skill type:
- **Content/marketing skills** (has voice component): `(accuracy*2 + completeness*1.5 + clarity + efficiency + voice) / 6.5`
- **Utility/tool skills** (no voice): `(accuracy*2 + completeness*1.5 + clarity + efficiency) / 5.5`

For skills scoring below 4.0, write specific improvement recommendations with concrete examples.

#### 2d. Security Assessment

Phase 1 now scans workspace files for common secret patterns (sk-, ghp_, AIzaSy, Bearer tokens, hex private keys, etc.). In Phase 2, go deeper:

- Review any secrets the script found in workspace files. Are they real credentials or false positives (e.g., example/placeholder values)?
- Check if any skill `scripts/` contain hardcoded credentials or API URLs with embedded tokens
- Check if `.env` files exist inside skill directories
- Look for credentials in cron job prompts (some prompts inline API keys instead of referencing env vars)
- Check if any workspace knowledge files contain customer data, passwords, or access tokens

## Output Format

### Phase 1 (script output)
```json
{
  "score": 82,
  "score_type": "structural_hygiene",
  "status": "healthy",
  "sections": {
    "security": {"score": 65, "finding_count": 3},
    "cron": {"score": 95, "finding_count": 1},
    "config": {"score": 88, "finding_count": 2},
    "skills": {"score": 80, "finding_count": 1}
  },
  "findings": [...]
}
```

### Phase 2 (your evaluation)

Present as a readable report to the user:

```
## ClawCheck Report

### Structural Baseline (Phase 1)
Overall: 82/100 (healthy)
Security: 65 | Cron: 95 | Config: 88 | Skills: 80

### Deep Quality Findings (Phase 2)

**Config:**
- Heartbeat prompt: 4/5 (clear but could add Telegram alert on critical)
- Model choices: 5/5 (opus primary, sonnet fallback, sonnet subagent)
- Compaction: 4/5 (reserveTokens=150k for 800k context = 19%, good)

**Cron (top concerns):**
- "Morning Brief" (3/5): prompt is 400 words but lacks output format spec
- "Bleeding Edge Scanner" (2/5): no safety guardrails, no error handling

**Skills (bottom 3):**
- marketing-automation: BROKEN (no SKILL.md)
- apple-notes (62/100 structural): [content evaluation]
- blucli (62/100 structural): [content evaluation]

### Recommended Actions (priority order)
1. [most impactful fix]
2. [next fix]
3. [next fix]
```

## Scoring Weights (Phase 1 script)

Security 30%, cron 25%, config 20%, skills 25%.

Skill structure formula: `(structure*2 + completeness*1.5 + clarity + efficiency) / 5.5 * 20`

## Remediation

For detailed fix patterns with real config examples, see `{baseDir}/references/remediation.md`.

Quick fixes for common findings:

### Inline secrets
```json
"GAMMA_API_KEY": {"source": "exec", "provider": "op-gamma", "id": "value"}
```

### Plaintext bot token
```json
"botToken": {"source": "exec", "provider": "op-telegram", "id": "value"}
```

### Missing heartbeat
```json
"heartbeat": {"every": "1h", "model": "sonnet", "prompt": "HEARTBEAT: Quick check..."}
```

### Missing timezone on cron
```json
"schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "Europe/Madrid"}
```

## Error Handling

- If OpenClaw dir not found: script exits with error JSON and exit code 1.
- If `openclaw.json` is missing or invalid: script exits with error JSON.
- If individual module fails: caught and reported as warning, other modules still run.
- If bundled skills dir not accessible: skipped silently.
- Phase 2 failures: if you can't read a file, note it and move on. Don't stop the whole audit.

## Non-Goals

- No direct edits to config or skills (report only, user decides)
- No network calls (everything is local file inspection)
- No overlap with `openclaw doctor` schema validation or channel connectivity checks
