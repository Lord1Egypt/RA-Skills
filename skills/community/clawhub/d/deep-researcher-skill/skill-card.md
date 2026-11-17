## Description:

Aggregates web, academic, video, and forum sources into structured research briefs, deep dives, comparisons, and temporal updates with source-quality and confidence checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffguides](https://clawhub.ai/user/geoffguides)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to direct an agent through multi-source research, source evaluation, bias checks, and structured reporting for decisions or content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags paywall-bypass instructions and routing URLs through third-party services without adequate safeguards.

Mitigation: Use only on publicly accessible material, do not use it to bypass paywalls or restricted access controls, and supervise research behavior closely.

Risk: Research tasks may involve private, signed, internal, or token-bearing URLs.

Mitigation: Do not provide sensitive URLs or credentials; keep optional API keys outside the repository or in a secret manager.

Risk: Multi-source synthesis can produce incorrect or misleading conclusions when source quality is weak or contradictory.

Mitigation: Require citations, confidence labels, and review of source quality before using outputs for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geoffguides/skills/deep-researcher-skill)
- [Publisher profile](https://clawhub.ai/user/geoffguides)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research reports with citations, confidence ratings, comparison tables, and optional configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source lists, confidence scores, source-quality tables, decision matrices, and suggested follow-up questions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
