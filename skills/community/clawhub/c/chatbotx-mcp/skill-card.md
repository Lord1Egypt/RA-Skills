## Description:

Use ChatbotX MCP tools to operate contacts, conversations, flows, broadcasts, sequences, analytics, and workspace automation from agentic IDEs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatbotx](https://clawhub.ai/user/chatbotx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect agentic IDEs to a ChatbotX workspace for contact management, conversations, analytics, broadcasts, flows, sequences, and workspace automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can affect live customer messaging and workspace settings when granted broad ChatbotX permissions.

Mitigation: Use read-only or narrowly scoped ChatbotX tokens by default, and require human approval before sends, broadcasts, publishes, deletes, member changes, integrations, or webhook changes.

Risk: Unpinned npx execution can run a package version that has not been reviewed for the target environment.

Mitigation: Prefer a pinned or pre-reviewed chatbotx-mcp package version for production or sensitive workspaces.

Risk: Workspace tokens can be exposed if copied into prompts, logs, generated documents, or committed configuration.

Mitigation: Keep ChatbotX API keys in environment variables or secret storage and avoid including them in prompts, logs, generated docs, or committed files.

## Reference(s):

- [ChatbotX MCP Skill Page](https://clawhub.ai/chatbotx/skills/chatbotx-mcp)
- [ChatbotX API Base URL](https://app.chatbotx.io/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ChatbotX workspace token and Node.js 18 or newer.]

## Skill Version(s):

1.1.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
