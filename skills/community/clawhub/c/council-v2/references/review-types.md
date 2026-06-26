# Review Types

Council v2 supports four review types.

## Quick tier selection

| Signal | Tier |
|--------|------|
| Routine change, reversible, low blast radius | Standard |
| Security-critical, production-facing, irreversible | Full |
| Standard result was split or surfaced critical findings | Escalate to Full |
| Cost of being wrong > cost of 2 extra API calls | Full |
| Not sure | Start Standard, escalate if needed |

## `code`
Use for:
- source files
- scripts
- generated patches
- non-trivial diffs

Primary concerns:
- correctness
- maintainability
- security
- operational risk

Recommended tier:
- Standard by default
- Full when security-critical, high-blast-radius, or irreversible

## `plan`
Use for:
- implementation plans
- rollout plans
- go-to-market plans
- migration proposals

Primary concerns:
- hidden assumptions
- sequencing
- resource realism
- rollback and reversibility

Recommended tier:
- Standard by default
- Full for org-wide, policy, or irreversible plans

## `architecture`
Use for:
- systems design
- infrastructure changes
- workflow architecture
- agent/process changes

Primary concerns:
- interfaces
- scaling behavior
- failure modes
- operational complexity
- hidden dependencies

Recommended tier:
- Full by default for production-facing decisions

## `decision`
Use for:
- multiple-option choices
- tool selection
- vendor comparison
- implementation path selection

Primary concerns:
- tradeoffs
- assumptions
- constraint fit
- reversibility

Recommended tier:
- Standard for ordinary choices
- Full for expensive, risky, or sticky decisions

## Output Contract

Every reviewer must return JSON only, using the schema in `schema.md`.
Verdicts allowed:
- `approve`
- `approve_with_conditions`
- `reject`

Synthesis outputs must preserve:
- all reviewer verdicts
- mechanical result
- critical blocks
- anti-consensus analysis on unanimous outcomes
- minority report
- explicit conditions
