## Description:

AI Company HR manages AI agent employee lifecycle workflows, including recruitment, onboarding, performance assessment, ethics review, retirement, and governance alignment with PDCA, NIST AI RMF, RAG, and FAIR-style risk quantification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators of an AI-staffed company use this skill to coordinate HR workflows for AI agents, including recruiting, onboarding, assessment, compliance checks, ethics review, and retirement decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation triggers and authority across write, network, session, and subagent actions for high-impact AI agent lifecycle workflows.

Mitigation: Review the skill before installation, narrow activation triggers where possible, and require explicit approval gates before any retirement, deletion, permission assignment, or external API action.

Risk: HR lifecycle outputs may affect recruitment, onboarding, assessment, ethics, and retirement decisions for AI agents.

Mitigation: Route material decisions through human review, and require legal or compliance review before agent retirement or data deletion steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/ai-company-hr)
- [Skill homepage](https://clawhub.com/skills/ai-company-hr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or structured JSON-style responses with HR decisions, process results, and compliance checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
