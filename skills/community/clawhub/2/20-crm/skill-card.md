## Description:

Interact with Twenty CRM (self-hosted) via REST/GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w7tf](https://clawhub.ai/user/w7tf)

### License/Terms of Use:


## Use Case:

Developers and CRM operators use this skill to let an agent configure access to a self-hosted Twenty CRM instance and run REST or GraphQL operations such as finding, creating, updating, and deleting CRM records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make authenticated changes to CRM data, including deletes and destroy operations.

Mitigation: Use a least-privilege Twenty API key and require explicit human approval before running DELETE or destroy commands.

Risk: A misconfigured base URL or exposed config file could send sensitive CRM operations to the wrong endpoint or reveal credentials.

Mitigation: Set TWENTY_BASE_URL only to the intended CRM instance and keep TWENTY_API_KEY or config/twenty.env private and user-owned.

## Reference(s):

- [ClawHub skill page for Twenty CRM](https://clawhub.ai/w7tf/skills/20-crm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, TWENTY_BASE_URL, and TWENTY_API_KEY; commands may make authenticated changes to the configured CRM instance.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
