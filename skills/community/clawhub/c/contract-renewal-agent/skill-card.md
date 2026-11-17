## Description:

Manages contract renewal records, reminders, status updates, and renewal proposal drafting with local JSON storage and no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cunningham050503-ops](https://clawhub.ai/user/cunningham050503-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Business, legal, procurement, and account teams use this skill to track contract expirations, monitor renewal windows, update lifecycle status, and draft renewal proposal text from stored contract records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive contract or financial data may be stored in weakly protected local JSON.

Mitigation: Use the skill only where local user access is trusted, avoid storing unnecessary confidential details, and protect the local workspace.

Risk: Contract records can be permanently deleted without confirmation.

Mitigation: Keep backups of the local contract database and review delete requests before running them.

## Reference(s):

- [Contract Renewal Agent ClawHub Page](https://clawhub.ai/cunningham050503-ops/skills/contract-renewal-agent)
- [Contract Renewal Strategies](references/renewal_strategies.md)
- [Contract Renewal Proposal Templates](references/contract_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance, JSON CLI output, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, and delete contract records in a local JSON database under ~/.openclaw/workspace/contract-renewal-agent/contracts.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
