## Description:

Create and publish social media launches via the Dropspace API, including launch creation, scheduling, persona-based content generation, and post analytics across major social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jclvsh](https://clawhub.ai/user/jclvsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media teams use this skill to create, review, schedule, publish, monitor, and manage Dropspace launches through API-oriented guidance and shell command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to publish, schedule, retry, or delete real social posts through the Dropspace API.

Mitigation: Confirm every live publish, scheduled publish, retry, and post deletion before execution, and keep publish or delete scopes off the API key unless explicitly needed.

Risk: The skill points to an unpinned Dropspace MCP package.

Mitigation: Prefer direct API use or a pinned, reviewed MCP package version, and run any MCP server with minimal filesystem and environment access.

Risk: Broad API keys can expose account management, webhook, publish, and deletion capabilities.

Mitigation: Create a separate least-privilege Dropspace API key, typically limited to read, write, and generate scopes for draft-and-review workflows.

## Reference(s):

- [Dropspace documentation](https://www.dropspace.dev/docs)
- [Dropspace llms.txt](https://www.dropspace.dev/llms.txt)
- [Dropspace OpenAPI specification](https://www.dropspace.dev/openapi.json)
- [ClawHub Dropspace skill page](https://clawhub.ai/jclvsh/skills/dropspace)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DROPSPACE_API_KEY environment variable for live API operations.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
