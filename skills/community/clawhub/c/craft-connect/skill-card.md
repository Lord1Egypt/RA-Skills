## Description:

Craft Connect lets agents read, create, update, search, organize, and format Craft documents, tasks, folders, collections, comments, and uploads through the Craft Connect REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwnex](https://clawhub.ai/user/hwnex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a connected Craft space: search documents, create or modify content, manage tasks, folders, collections, comments, uploads, and apply Craft-specific formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRAFT_API_URL contains an embedded link token and acts like a credential with read/write access to the connected Craft space.

Mitigation: Keep TOOLS.md private, do not commit the URL, and treat the value like a password.

Risk: The skill can modify or delete documents, blocks, tasks, folders, collection items, schemas, comments, and uploaded files.

Mitigation: Review destructive actions, uploads, and collection schema changes before execution, and prefer scoped searches or explicit target IDs when practical.

## Reference(s):

- [Craft Formatting Cheatsheet](references/formatting-cheatsheet.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CRAFT_API_URL as the Craft Connect API base URL and returns Craft API responses as JSON or formatted document content.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
