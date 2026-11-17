## Description:

AllOurThings helps agents add, find, update, search, and delete household or personal inventory records and attachments in a user's configured vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matt-harding](https://clawhub.ai/user/matt-harding)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage a household or personal inventory vault, including possessions, warranties, purchase history, locations, and related attachments. It is intended for inventory questions and record changes when ALLOURTHINGS_DATA_DIR is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is installed through unpinned npm package resolution.

Mitigation: Prefer a pinned and reviewed package version before deployment.

Risk: The skill can delete inventory items and attachments from the configured vault.

Mitigation: Require explicit user confirmation before deleting items or attachments.

Risk: The MCP server accesses personal inventory records and attachment files.

Mitigation: Limit filesystem access to the ALLOURTHINGS_DATA_DIR vault and install only when the package source is trusted.

## Reference(s):

- [AllOurThings homepage](https://allourthings.io)
- [ClawHub skill page](https://clawhub.ai/matt-harding/skills/allourthings)
- [Publisher profile](https://clawhub.ai/user/matt-harding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger MCP operations that read, create, update, delete, or attach files in the configured inventory vault.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
