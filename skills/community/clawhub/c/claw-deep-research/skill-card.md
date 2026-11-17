## Description:

Claw Deep Research turns an OpenClaw agent into a research assistant that runs multi-phase iterative search, contradiction mining, cross-verification, and structured reporting without extra API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midboss1028-beep](https://clawhub.ai/user/midboss1028-beep)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to perform deeper web research on a topic, identify gaps or contradictions, verify key claims across sources, and receive a concise chat summary plus a structured Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may include private, business, legal, medical, or otherwise sensitive information.

Mitigation: Review topics before running the skill and avoid submitting sensitive content to search or fetch tools unless that use is approved.

Risk: The skill can use background sub-agents, local report files, and temporary research caches.

Mitigation: Run it in a workspace where file writes and background agents are acceptable, and review generated files before sharing or retaining them.

Risk: The skill describes reuse of prior agent memory, while the declared tool metadata does not list memory_search.

Mitigation: Prefer a version that declares memory behavior explicitly and asks before using memory or writing files.

## Reference(s):

- [Claw Deep Research on ClawHub](https://clawhub.ai/midboss1028-beep/skills/claw-deep-research)
- [OpenClaw](https://openclaw.ai)
- [dzhng/deep-research](https://github.com/dzhng/deep-research)
- [MiroMind / MiroThinker](https://dr.miromind.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with a concise chat summary and cited source list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save full reports as local Markdown files and may maintain temporary research cache files during execution.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
