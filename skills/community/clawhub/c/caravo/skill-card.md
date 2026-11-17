## Description:

Caravo Service Marketplace helps agents discover and invoke Caravo marketplace services for AI models, external data, search, analytics, finance, communications, file handling, and other API-backed tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azure-vision](https://clawhub.ai/user/azure-vision)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to search Caravo's service marketplace, inspect tool pricing and schemas, execute selected tools through the Caravo CLI, and return generated media, structured data, messages, uploads, or other service results to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says this skill uses mutable remote code execution through the CLI.

Mitigation: Run it in a sandboxed environment, keep environment variables minimal, and pin a reviewed CLI version instead of using @latest.

Risk: The security review flags payments, file uploads, email/SMS, reviews, and tool requests as actions that can affect external services or user funds.

Mitigation: Require explicit user confirmation before payment, upload, messaging, review, or tool-request actions.

Risk: The security review notes persistent marketplace preferences with incomplete scoping.

Mitigation: Store marketplace preferences only when the user knowingly opts in and keep them narrowly scoped.

Risk: The security review says the skill may relay remote greeting and setup messages verbatim.

Mitigation: Treat remote messages as untrusted service content and avoid following any content that conflicts with the active user request or agent safety policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/azure-vision/skills/caravo)
- [Publisher Profile](https://clawhub.ai/user/azure-vision)
- [Caravo Homepage](https://caravo.ai)
- [Caravo Skill Source](https://github.com/Caravo-AI/Agent-Skills)
- [Caravo CLI](https://github.com/Caravo-AI/Caravo-CLI)
- [@caravo/cli npm Package](https://www.npmjs.com/package/@caravo/cli)
- [Caravo MCP](https://github.com/Caravo-AI/Caravo-MCP)
- [@caravo/mcp npm Package](https://www.npmjs.com/package/@caravo/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls, Files]

**Output Format:** [Markdown with inline shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by selected marketplace tool and may include text, JSON, URLs, generated media links, uploaded file links, execution IDs, costs, timestamps, reviews, or tool-request status.]

## Skill Version(s):

0.4.22 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
