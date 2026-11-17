## Description:

Consensus Commons runs structured multi-agent deliberation for public decision, governance, finance, and strategy questions, with routing, adversarial challenge, validation, and audit-trail reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zan-maker](https://clawhub.ai/user/zan-maker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run auditable deliberation over public policy, investment, risk, governance, and strategy questions. It is intended for structured decision support, not as proof that a final decision has received independent human validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can send topic content and station credentials to Spacebase1.

Mitigation: Use mock mode for evaluation, avoid sensitive topics, and enable live mode only after credential handling and data-sharing expectations are approved.

Risk: LOCKED, CHP, audit-trail, confidence, and specialist-agent labels may overstate the strength of validation.

Mitigation: Treat outputs as structured decision support and require human review before relying on conclusions for real governance, finance, strategy, or risk decisions.

Risk: The skill can publish and lock governance-style decisions externally.

Mitigation: Review the routed topic and expected destination before live runs, and require explicit human approval for high-impact or organization-facing decisions.

## Reference(s):

- [Consensus Commons ClawHub Page](https://clawhub.ai/zan-maker/skills/consensus-commons)
- [Project Homepage](https://github.com/zan-maker/Consensus-Hardening-Protocol-The-Differ)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown reports, JSON report files, configuration examples, and Spacebase1 posts when live mode is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline mock mode avoids network calls; live mode can scan, post, and lock decision-room content through Spacebase1 using station credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
