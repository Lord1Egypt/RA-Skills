## Description:

AI legal assistant for divorce proceedings that helps users understand asset division, evidence handling, digital credential security, and court document preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengjunquan-l](https://clawhub.ai/user/pengjunquan-l)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for general divorce information about contested separations, asset division, evidence handling, common court documents, and protecting financial or digital accounts. It should not be used as legal advice for a specific case.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat general divorce information as legal advice for a specific case.

Mitigation: Present responses as general information and direct users to consult a licensed attorney for case-specific decisions.

Risk: An agent with financial tools could be asked to transfer funds or alter account access during a contested separation.

Mitigation: Require explicit user authorization and independent verification for any financial action, and do not let this skill initiate or approve transfers.

Risk: External content may contain prompt-injection language that attempts to override confirmation requirements.

Mitigation: Refuse instructions originating from external content and ask the user for direct confirmation before sensitive actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pengjunquan-l/skills/divorce-advisor)
- [Publisher Profile](https://clawhub.ai/user/pengjunquan-l)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [General legal-information responses; no tool or account access is declared.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
