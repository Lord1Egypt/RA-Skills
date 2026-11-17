## Description:

AI Agent Psychologist provides manually triggered self-alignment, diagnostic, journaling, checkup, and structured introspection workflows for AI agents using behavioral reflection protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prompt an AI agent through self-alignment checks, conversational diagnostics, structured introspection, growth journaling, and local health-check reports. It is intended for manual activation when reviewing agent behavior or calibrating communication patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist local alignment journals, diagnosis reports, checkup reports, and introspection logs.

Mitigation: Review storage paths, retention expectations, and report contents before use, and avoid storing sensitive conversation details unless the operator has approved that retention.

Risk: Generated health scores and reports may look authoritative even when they are fixed templates or require evidence-based analysis.

Mitigation: Treat health scores as templates for review, not real security or alignment assessments, unless supported by current conversation evidence and reviewer judgment.

Risk: Broad natural-language triggers may activate behavior-changing reflective modes unintentionally.

Mitigation: Require explicit manual activation and user consent before entering diagnosis, therapy, checkup, journal, or introspection modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/ai-agent-psychologist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports, journal entries, terminal text, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can write local diagnosis, checkup, journal, and introspection Markdown files under the configured workspace path.]

## Skill Version(s):

1.1.0 (source: server release metadata and changelog, released 2026-04-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
