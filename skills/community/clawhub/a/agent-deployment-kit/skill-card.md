## Description:

Replicate one agent across N clients without drift - one context source, a generator that refuses unknowns. Use when duplicating an agent deployment. Trigger on "duplicate this agent", "same bot new client", "the agent named the wrong client".

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to duplicate an agent deployment across clients without drift by maintaining one questionnaire, generating installs from templates, and auditing guardrails before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the methodology as a ready-made generator and miss destructive deploy or privacy guards.

Mitigation: Before live use, verify that any generated kit refuses unresolved sentinels, blocks unguarded deletes or overwrites, and requires explicit deploy approval.

Risk: Rendered agents that process inbound DMs can handle personal data without a real legal basis or retention process.

Mitigation: Require named LEGAL_BASIS, DATA_MINIMISATION, and DATA_RETENTION values, and ship a retention job that actually deletes covered data.

Risk: Secrets or backup copies may expose credentials or personal data if handled like normal repo files.

Mitigation: Keep real secrets out of the repository, transfer credentials out of band, treat backups as cleartext sensitive data, and purge backups after validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/agent-deployment-kit)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; shipped examples are fictional context and secrets templates.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
