---
name: council-v2
description: >
 Multi-model council review that spawns 3-5 independent AI reviewers and applies
 mechanical synthesis — votes decide, not orchestrator opinion. Use when you need
 a second opinion on code before merge, a pre-flight check on a plan, an architecture
 review for a technical decision, or a structured critique of options. Also use when
 someone says "is this safe to ship?", "get me a sanity check", "review this with
 multiple models", or "I want adversarial feedback." Do not use for trivial edits
 or low-stakes decisions where the overhead exceeds the risk.
version: 2.0.3
---

# Council v2

A hardened OpenClaw skill for multi-model council reviews.
It dispatches independent reviewers, collects structured JSON, and applies a
**mechanical synthesis protocol** so the final verdict is driven by votes and
critical findings — not orchestrator vibes.

Primary entrypoint: `bash skills/council-v2/scripts/council.sh review <type> [file]`

## When to Use

Use when a single model reviewing its own work is not enough:
- Code review before merge or deployment
- Plan review before committing resources
- Architecture review for important technical decisions
- Decision review when multiple plausible options exist
- Security-sensitive or irreversible choices
- Pre-flight review, adversarial critique, or second-opinion work

## When Not to Use

Do **not** use for:
- One-line fixes or trivial edits
- Low-stakes decisions where overhead exceeds risk
- Purely factual lookups with no judgment call
- Work already reviewed recently with no material change

## Council Shape

Two tiers are supported:
- **Standard** — 3 reviewers for routine code, plan, and decision reviews
- **Full** — 5 reviewers for high-stakes, security-sensitive, or irreversible choices

### Tier selection heuristic

Use **Standard** when: routine code changes, internal plans, reversible decisions,
low blast radius. Use **Full** when: security-critical, production-facing architecture,
irreversible commitments, high cost of being wrong, or when you want maximum coverage.

When in doubt, start Standard. Escalate to Full if the Standard result is split or
if critical findings surface that need more perspectives.

### Cost note

Full Council runs 5 model calls instead of 3. That is ~1.7x the token cost of Standard.
Use Full when the cost of a bad decision exceeds the cost of the extra API calls —
which for security, architecture, and irreversible choices, it almost always does.

Detailed role composition and synthesis rules live in:
- `references/review-types.md`
- `references/role-prompts.md`
- `references/synthesis-rules.md`

## Review Types

| Type | Typical use |
|------|-------------|
| `code` | Source files, scripts, patches, PR diffs |
| `plan` | Proposals, project plans, rollout plans |
| `architecture` | Systems design, infra decisions, workflows |
| `decision` | A/B/C choices with tradeoffs |

Definitions: `references/review-types.md`

## Quick Start

```bash
# Standard code review
bash skills/council-v2/scripts/council.sh review code src/auth.py

# Force full plan review
bash skills/council-v2/scripts/council.sh review plan proposal.md --tier full

# Architecture review from stdin
cat design.md | bash skills/council-v2/scripts/council.sh review architecture --tier full

# Decision review with options
bash skills/council-v2/scripts/council.sh review decision options.md --options "SQLite,Postgres,Cloud SQL"

# Emit orchestration plan as JSON
bash skills/council-v2/scripts/council.sh review code src/auth.py --format json
```

## How It Works

1. Loads content from file or stdin
2. Selects Standard or Full tier
3. Builds reviewer prompts from `references/role-prompts.md`
4. Emits an orchestration plan suitable for `sessions_spawn`
5. Collects reviewer JSON outputs
6. Runs `python3 scripts/synthesize.py ...`
7. Returns synthesis with mechanical result, minority report, and conditions

## Interpreting Results

The synthesizer returns structured JSON and a meaningful exit code:

| Exit code | Meaning | What to do |
|-----------|---------|------------|
| `0` | **Approve** — clear majority, no criticals | Ship it |
| `1` | **Reject or Blocked** — majority rejected or a critical finding blocked | Address the critical findings or rethink the approach |
| `2` | **Approve with conditions** — mixed or conditional majority | Fix the flagged conditions, then re-review or proceed with documented risk |
| `3` | **Error** — invalid input or synthesis failure | Check reviewer JSON for malformed output; see error handling below |

### Reading the synthesis output

- **mechanical_result**: The vote-driven verdict. This is the answer.
- **critical_blocks**: Any critical findings that auto-blocked approval. Address these first.
- **conditions**: Aggregated recommendations from warning-level findings. These are your fix list.
- **minority_report**: The strongest dissent from the majority. Read this even if you agree with the majority — it is often where the best insight lives.
- **anti_consensus_check**: Fires on unanimous decisions. Treat the counterargument seriously.

## Error Handling

### Reviewer returns invalid JSON

`synthesize.py` validates every reviewer output against required fields. If a reviewer
returns malformed JSON, synthesis exits with code 3 and prints an error message.

What to do:
1. Check the raw reviewer output for the failing model
2. Re-run that single reviewer (the orchestration plan shows which models to dispatch)
3. If the model consistently fails, substitute it — see model override flags below

### Provider is down or times out

If a provider fails to respond, the review set will be incomplete. Run synthesis on
whatever outputs you have — a 2-of-3 Standard review is still useful. Note the missing
reviewer in your assessment.

### Model override flags

Override any model at the command line:
```bash
bash skills/council-v2/scripts/council.sh review code src/auth.py \
 --opus claude-sonnet-4 \
 --gpt gpt-4.1 \
 --grok grok-3
```

Available flags: `--opus`, `--gpt`, `--grok`, `--deepseek`, `--gemini`

## Model Diversity

The council's value comes from **different providers with different training data and
different biases** reviewing the same decision. The specific model versions (Opus,
GPT-5.4, Grok 4, etc.) matter less than the diversity. Swap in whatever top-tier
models you have access to — what matters is that they are not all from the same
provider.

## Retrospectives

`scripts/retro.sh` generates a structured retrospective template for reviewing past
council decisions against actual outcomes.

```bash
# Review the 5 most recent decisions in a directory
bash skills/council-v2/scripts/retro.sh ./council-outputs/ 5
```

### When to run retros

Run monthly, or after any decision where the outcome surprised you. The retro surfaces:
- Which reviewers provided signal vs. noise
- Whether critical findings were real or false alarms
- Whether synthesis preserved minority views accurately
- Prompt changes to consider for role-prompts.md

Feed retro findings back into `references/role-prompts.md` to calibrate the council.

## Notes

- Requires `bash`, `python3`, and OpenClaw reviewer dispatch capability
- Model aliases can be overridden — see model override flags above
- Synthesis rules are documented in `references/synthesis-rules.md`

## References

- `references/review-types.md` — review type definitions and tier recommendations
- `references/role-prompts.md` — reviewer role prompts and shared output instructions
- `references/schema.md` — JSON schemas for reviewer output and synthesis output
- `references/synthesis-rules.md` — mechanical synthesis protocol and edge cases
