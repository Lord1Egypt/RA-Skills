## Description:

EU AI Act risk classification, Article 12 compliance logging, and self-assessment reports - deadline August 2, 2026.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to classify EU AI Act risk, inspect Article 12 logging mappings, and request compliance assessment artifacts for AI systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may send secrets, personal data, regulated data, proprietary controls, or detailed internal architecture to external endpoints.

Mitigation: Use approved test descriptions or sanitized system summaries unless data sharing with the provider has been reviewed and authorized.

Risk: Compliance outputs may be mistaken for legal advice or a final regulatory determination.

Mitigation: Treat generated classifications and reports as triage and documentation assistance, then review them with qualified compliance or legal stakeholders before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drivenbymyai-max/skills/eu-ai-compliance)
- [Publisher profile](https://clawhub.ai/user/drivenbymyai-max)
- [Compliance web interface](https://soulledger.sputnikx.xyz/compliance)
- [Compliance API base URL](https://soul.sputnikx.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill points agents to external compliance endpoints that may return risk classifications, mappings, self-assessments, declarations, technical documentation, or bundled reports.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
