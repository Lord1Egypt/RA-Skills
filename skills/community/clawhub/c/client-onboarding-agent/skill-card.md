## Description:

Client Onboarding Agent guides consultants through structured AI agent deployment onboarding, including business diagnostics, constraint analysis, deployment planning, completion contracts, tiered advisory controls, and a six-week client narrative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants and automation service providers use this skill to onboard clients for AI agent deployments by mapping pain points, workflows, constraints, and phased deployment plans. It is not intended for self-service SaaS onboarding or consumer product onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client onboarding may involve confidential or regulated business data.

Mitigation: Collect and process sensitive client information only with permission, and follow the skill's constraint-identification step for regulatory, data, and audit requirements.

Risk: High-impact automations such as payments, filings, contracts, or regulated work could cause harm if executed without oversight.

Mitigation: Use the skill's tiered advisory mode so high-risk tasks require explicit human approval and restricted tasks remain draft-only.

Risk: Incorrect scope or premature automation promises could create client expectations that the deployment cannot meet.

Mitigation: Use the four-round diagnostic process, completion contracts, staged approval, and timeout bounds before treating a deployment phase as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/client-onboarding-agent)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with diagnostic questions, matrices, timelines, and checklist templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory onboarding artifacts and human-reviewed deployment plans; no bundled code or hidden execution behavior is included.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
