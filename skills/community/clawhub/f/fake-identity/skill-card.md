## Description:

Generate realistic fake identities from multiple countries and ethnicities after collecting country or ethnicity, gender, and explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshsojitra](https://clawhub.ai/user/adarshsojitra)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to generate a realistic fictional identity profile, including demographic details, addresses, government ID-like fields, and a temporary email account after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce realistic personal details, government ID-like fields, and mailbox credentials that may enable impersonation or account abuse.

Mitigation: Constrain deployments to clearly fictional placeholders, reserved example domains, and block live mailbox creation or usable credentials.

Risk: The skill asks agents to create a fresh email account through mail.tm.

Mitigation: Require tool policy review before enabling external API access and avoid creating accounts for use on real services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshsojitra/skills/fake-identity)
- [mail.tm](https://mail.tm)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown profile with labeled sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-selected country or ethnicity and gender plus explicit confirmation before generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
