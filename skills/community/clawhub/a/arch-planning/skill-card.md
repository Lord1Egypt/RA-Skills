## Description:

A Chinese-language conversational architecture planning skill that helps users clarify system architecture, technology selection, solution design, requirements analysis, and technical planning through staged dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical leads use this skill to turn unclear architecture or planning questions into scoped requirements, constraints, system decomposition, trade-off decisions, ADR notes, and validation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-Chinese users may have difficulty reviewing or applying the skill guidance accurately.

Mitigation: Translate or have a Chinese-proficient reviewer inspect the guidance and templates before operational use.

Risk: Architecture recommendations can be incomplete or misleading if users skip staged clarification, assumption testing, or validation planning.

Mitigation: Follow the skill's gated workflow, document ADRs, and validate low-confidence assumptions with POCs, stress tests, or fallback plans before implementation.

## Reference(s):

- [Requirements Clarification Checklist](references/requirements-framework.md)
- [Technology Trade-off Matrix](references/tradeoffs-matrix.md)
- [Architecture Risk Checklist](references/risk-checklist.md)
- [Architecture Decision Record Template](references/adr.md)
- [Assumptions and NFR Thresholds](references/assumptions-nfr.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured planning notes, ADR entries, checklists, and concise architecture summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language conversational guidance; no shell commands, code execution, or privileged actions are described by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
