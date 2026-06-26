# VNext review — 2026-03-12

Scope: restrained product/architecture review after v1 scaffold + QA.

## Recommended next-version ideas

### 1. Canonical citation normalization
Highest leverage product improvement.

Why:
- Current citations are often Google/Vertex grounding redirect URLs, which are bad for human trust, dedupe, downstream `web_fetch`, and durable notes.
- The skill’s output is already JSON-first, so citation quality is a large fraction of perceived quality.

What to do:
- Prefer canonical publisher/source URLs if grounding metadata exposes them.
- If not directly exposed, add a small deterministic normalization layer for known redirect patterns.
- Preserve raw grounding URL separately if needed for debugging, but make the default `citations[].url` the best canonical URL available.

Why this beats other polish:
- Improves every successful query, not just failure cases.
- Makes the skill much more usable as an orchestration primitive.

### 2. Deterministic fallback test harness
Highest leverage engineering improvement.

Why:
- The core promise of this skill is model routing + fallback.
- Live/manual QA proved the concept, but the fragile part is still mostly tested by ad hoc runs.
- Without deterministic tests, future model-routing edits can silently regress stop/fallback boundaries.

What to do:
- Add a checked-in test harness that monkeypatches or injects a fake `call_gemini`.
- Cover only the decision logic, not live API behavior.
- Minimum matrix:
  - retryable 429/unavailable -> continue fallback
  - non-retryable local/config error -> stop immediately
  - all candidates fail -> `all_models_failed`
  - `usage.attempted_models` order remains stable
  - escalation object is set only for suspicious/systemic cases

Why this matters:
- Lets the repo evolve model mappings safely.
- Reduces dependence on quota and current upstream availability for confidence.

### 3. Lightweight model recon automation
Worth doing, but smaller than the two items above.

Why:
- The current repo already discovered that UI labels and callable IDs drift.
- That drift is exactly the kind of thing that quietly rots a routing skill.

What to do:
- Add a small script that lists available models and optionally probes a curated candidate set.
- Output a compact snapshot usable to refresh `references/model-id-recon.md` and spot dead candidates.
- Keep it advisory; do not auto-rewrite production mappings yet.

Why only lightweight:
- Full self-mutating routing is overkill for now.
- A cheap recon/report step gets most of the value with less risk.

## Safe to defer

- Richer escalation UX such as prefilled GitHub issue bodies/titles. Current escalation shape is already adequate for v1.
- Broader mode surface or advanced tuning flags. The skill wins by being narrow and predictable.
- Adding `*-latest` rolling aliases as primary routing targets. Nice for experimentation, but pinned IDs are the safer default.
- True "deep" tier redesign with Pro models. That is a product/billing decision, not a near-term architecture must-have.

## Bottom line

If only one vNext item gets built, make it canonical citation normalization.
If two get built, add deterministic fallback testing.
Model recon automation is good third priority, but safe to stage after the first two.
