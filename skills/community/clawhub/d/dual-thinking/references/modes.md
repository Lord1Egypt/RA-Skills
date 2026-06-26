# Modes
#tags: skills review

## Deterministic router contract
Route in this order:
1. when the user explicitly requested alternation before round 1, set `ORCHESTRATOR_MODE: multi` and continue routing semantic intent to determine `MODE`
2. `analysis-only` when the user explicitly requested critique without mutation
3. skill-family modes when the topic is a skill or skill-adjacent artifact
4. artifact modes for non-skill artifacts
5. `general-decision-review` otherwise

The self-evolution lens is stance logic inside the routed mode, not a new public mode.

## skill-family routing
- `skill-rewrite`: concrete rewrite requested
- `skill-hardening`: runtime, safety, weak-model flow, or operability tightening requested
- `skill-publish-readiness`: packaging, release, distribution, share, or publish gate requested
- `weak-model-optimization`: weak-model clarity specifically requested
- `skill-review`: the default skill-family mode if none of the above are more specific

## Publish-scope rule
- publish, release, and package gates are required only in `skill-publish-readiness`
- in `skill-review`, `skill-rewrite`, `skill-hardening`, and `weak-model-optimization`, run publish checks only if the user explicitly asked for shipping, distribution, packaging, or readiness
- `analysis-only` is a valid mode and may be chosen directly by user intent or later as a bounded fallback

## Orchestrator mode
- `local`: no external consultant; set `ORCHESTRATOR: local`; produce `SELF_POSITION`; do self-synthesis; do not output `CONSULTANT_QUALITY`
- `api`: one external consultant used serially; round 2+ for the same topic must reuse the same chat or session by default so that consultant sees prior rounds in that same chat; open a fresh chat only for explicit recovery when the intended chat is broken, polluted, or context-degraded
- `multi`: alternating orchestrators explicitly requested before round 1; alternate by round, keep one persistent chat per orchestrator, produce one `SELF_POSITION` for the current artifact state before each consultant-bearing round, carry the patched artifact into the next orchestrator round, and preserve a `STATE_SNAPSHOT` for recovery between orchestrator turns; do not default to fresh-chat-per-round behavior

## Session naming rule
Use a deterministic session key per topic and orchestrator:
- format: `dt-<topic-slug>-<yyyymmdd>-<orchestrator>`
- reuse that same key for later rounds with the same topic and orchestrator
- only create a recovery variant when continuity is broken and the original session cannot be safely resumed or the consultant has clearly degraded under context load and is no longer reviewing the visible same-topic chat honestly

## Deliverable rule
Every mode must still emit the minimum round block.
Add extended fields when they help, and emit patch state whenever a real fix was accepted, deferred, or blocked.
