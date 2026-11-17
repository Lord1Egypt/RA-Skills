## Description:

Interact with Coda.io docs, tables, rows, pages, and automations via the Coda REST API v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonfunk](https://clawhub.ai/user/simonfunk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read, write, update, and delete Coda docs, tables, rows, pages, permissions, publishing settings, automations, and analytics through the Coda REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute live Coda delete, sharing, publishing, permission, and automation actions.

Mitigation: Manually confirm any destructive, permission-changing, publishing, sharing, or automation action before execution.

Risk: The skill requires a Coda API token that may grant access to sensitive docs.

Mitigation: Use the least-privilege token or account available and prefer read-first workflows before allowing writes.

## Reference(s):

- [Coda API v1 Endpoint Reference](artifact/references/api-endpoints.md)
- [Coda REST API v1](https://coda.io/apis/v1)
- [Coda API Token Settings](https://coda.io/account)
- [ClawHub Skill Page](https://clawhub.ai/simonfunk/skills/coda-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CODA_API_TOKEN environment variable and can produce live Coda API calls through the bundled shell helper.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
