# Skill Design Pattern: Start Here Before Requirements

A recurring usability failure in skills that target users who do not yet know what they need:

> The skill opens by demanding a filled template. Users with no data abandon the skill instead of starting.

This has been confirmed in production with `agent-cost-eval-kit` v1.x and applies to any eval, audit, diagnostic, or evidence-gathering skill.

## The Failure Mode

1. Skill activates (e.g., `eval agent cost change`)
2. Skill presents "Required Input" with a structured before/after template
3. User has no data, does not know where to find it, or cannot fill the template
4. User abandons or reports the skill as "not working"

The skill is not broken — it is designed for the wrong entry point.

## The Correct Pattern: Start Here

Structure every evidence-gathering / eval skill with this order:

### Layer 1 — Start Here (not "Required Input")
- Lowest friction entry point
- Accepts any level of completeness — partial data, no data, one sentence, logs, mental description
- Explicitly states: "If you do not know where to find before/after data, say so. This skill will first produce an Evidence Collection Plan."
- Gives one minimal example showing what "almost nothing" looks like
- Never demands a template as the first output

### Layer 2 — What You Will Get
- Clear list of possible outputs, ordered by evidence sufficiency:
  - Evidence Status (No Baseline Yet / Partial Evidence / Ready for Quick Evaluation / Ready for Full Evaluation / Unsafe to Judge)
  - Evidence Collection Plan (only if evidence is missing)
  - Before/After Summary (only if evidence is available)
  - Decision (only if evidence is sufficient)
  - Recommended Next Action (always)
  - Copy-Paste Evidence Request (adapted to user situation)

### Layer 3 — Evidence Collection Plan
- Only appears when evidence is missing
- Gives the smallest next data to collect — not a full template
- Asks for the next most useful evidence only
- Avoids overwhelming the user

### Layer 4 — Decision
- Only reached when evidence is sufficient
- Returns Keep / Revert / Narrow / Needs More Samples / Unsafe to Judge

## Why This Works

Users who have data will provide it and move to the decision.
Users who have no data will get a plan, not a rejection.
The skill meets users at their actual knowledge state, not at the knowledge state the author assumed.

## When to Use This Pattern

Apply this pattern to skills that:
- Activate via a user-initiated evaluation trigger (e.g., `eval X`, `audit X`, `diagnose X`)
- Target users who may not have structured before/after data at activation time
- Serve a decision-making purpose (keep/revert/narrow/test-further)
- Are read-only (not auto-fix or auto-apply)

Do NOT apply this pattern to:
- Skills that are purely informational (give me news, summarize this doc)
- Skills where the input IS the complete evidence (paste your code, paste your error)
- Skills that do not have a "do I have enough data to decide" problem

## Related Skills

- `agent-cost-eval-kit` — first production use of this pattern, v2.0.0+
- `investment-research-core` — also uses evidence-first structure; confirm it follows Start Here pattern