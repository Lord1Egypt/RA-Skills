## Description:

Atlas Tracker helps agents read, create, and update Atlas Tracker (RedForester) mindmap branches, typed nodes, link nodes, attachments, and comments through Atlas Tracker MCP and OpenClaw tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[didro](https://clawhub.ai/user/didro)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent navigate Atlas Tracker maps, inspect branches and node schemas, and make controlled updates to nodes, links, attachments, and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install and run a local MCP server and OpenClaw plugin from outside the released artifact.

Mitigation: Use server and plugin files only from a verifiable official source, inspect source and lockfiles, and avoid enabling the systemd service until the code is trusted.

Risk: Atlas Tracker credentials and local API keys are required for the MCP server and plugin.

Mitigation: Treat AUTH_HEADER and API_KEY as secrets, keep them out of prompts and logs, and scope the Atlas Tracker account to the minimum access needed.

Risk: The upload workflow can attach local files to Atlas Tracker nodes.

Mitigation: Confirm the absolute file path and data sensitivity before calling upload tools.

Risk: Write operations can alter map branches, typed properties, links, and comments.

Mitigation: Read the branch first, verify full map and node UUIDs, and submit only the smallest necessary create, update, or delete arrays.

## Reference(s):

- [Atlas Tracker REST API Patterns](references/api-patterns.md)
- [Atlas Tracker Node Types Guide](references/node-types-guide.md)
- [Atlas Tracker](https://app.redforester.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Atlas Tracker node URLs, full UUIDs, HTML-formatted node titles, typeProperties examples, and local file paths for upload workflows.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
