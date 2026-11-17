# Skill Card — decomtangle

*Format: NVIDIA Skill Card trust format (https://docs.nvidia.com/skills/skill-cards)*

## Description

Execution-time discipline for AI agents running multi-step procedures through
tool calls: one observable action per call, observe between steps, decompose
anything that would require embedding scripts or nested-quoted payloads in a
single call's arguments. Prevents the mega-tool-call anti-pattern that breaks
tool-call parsers and kills agent turns silently.

## Skill Version

0.1.0 (2026-07-06). Version carried in SKILL.md frontmatter per release.

## Status

Ready for use in any OpenClaw-style agent environment. Doctrine-only: safe to
install alongside any tool surface; especially recommended where local or
open-weight models execute browser automation or long tool chains.

## Owner

Jason Vaughan (`Jason-Vaughan` on ClawHub/GitHub). Accountable for content and
releases.

## License / Terms

MIT (see LICENSE). No warranty.

## Use Case

Operators of agent fleets whose agents execute multi-step, stateful procedures
(browser automation, API sequences, migrations), and who have observed or want
to prevent: silent mid-task stalls, opaque gateway 500s on tool calls,
shell-quoting failures in generated commands, or blind multi-action scripts
that leave systems in unknowable states. Pairs naturally with domain skills
that define WHAT to do (e.g. airbnb-gateway); DecomTangle governs HOW each
step is emitted.

## Deployment Geography

No geographic constraints; the skill is prose doctrine with no network or
data-handling behavior of its own.

## Requirements / Dependencies

- An OpenClaw-style agent runtime that loads skills. **Nothing else**: the
  skill declares no tools, no permissions, no environment variables, no
  network access, and no external services.

## Skill Output

Changed agent behavior only: atomic single-action tool calls, observation
between steps, payload-to-file handling of complex arguments, verified (not
assumed) side effects, and milestone reporting instead of silent procedure
endings.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Over-fragmentation (needless calls for trivial reads) | "When a single call IS enough" section defines the floor; pure one-shot reads and single idempotent commands stay single calls |
| Increased call count on constrained gateways | Calls are small and cheap relative to the stalls they prevent; targeted-read guidance keeps per-call output minimal |
| Doctrine ignored by very weak models | The rules are mechanical (quoting-depth tripwire, one-verb test) — designed to be followable by small models; observed to rescue a model that failed the same task un-decomposed |
| Skill conflicts with a domain skill's own procedure | DecomTangle is HOW-shaped, not WHAT-shaped; it composes with (and was extracted from incidents involving) domain procedures rather than overriding them |

## Ethical Considerations

None specific: the skill performs no actions itself and handles no data. It
inherits the ethics of whatever procedures the host agent runs; its
verify-before-claiming rule tends to increase operator visibility and
accountability.

## References

- `SKILL.md` — the five rules + working defaults
- `references/decomposition-heuristics.md` — boundary-finding tests + anti-pattern catalog
- `references/atomic-call-checklist.md` — per-call pre-flight check
- `examples/bad-mega-script-stall.md` — annotated real incident (2026-07-04 silent stall: unparseable mega-call → gateway KeyError/HTTP 500 → turn death with no terminal event)
- `examples/good-multicalendar-atomic.md` — the same procedure completed atomically on the same model
- **Release evidence (0.1.0)**: the good/bad example pair is drawn from a real production incident and its verified resolution on the publisher's reference deployment (multi-agent OpenClaw fleet operating a live Airbnb host account).
