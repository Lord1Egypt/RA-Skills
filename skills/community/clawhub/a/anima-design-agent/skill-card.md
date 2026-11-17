## Description:

Turns ideas into live, full-stack web applications with editable code, built-in database, user authentication, and hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use Anima to turn prompts, website URLs, Figma designs, and Anima Playground URLs into live applications or code that can be integrated into an existing project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger on broad build or design requests.

Mitigation: Confirm the user's intended Anima flow and destination before invoking Anima for ambiguous requests.

Risk: Prompts, Figma content, website content, or project context may be sent to Anima's external service.

Mitigation: Avoid private designs, internal websites, secrets, and regulated data unless external processing is explicitly approved.

Risk: The skill can publish live URLs.

Mitigation: Require explicit user confirmation before publishing any generated playground or application.

Risk: The workflow may run an unpinned third-party CLI.

Mitigation: Run CLI commands in an isolated project environment with a scoped API key and pin the package version where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dannyshmueli/skills/anima-design-agent)
- [Anima MCP Server Guide](https://github.com/AnimaApp/mcp-server-guide)
- [Anima CLI Documentation](https://github.com/AnimaApp/anima-cli)
- [Anima MCP Setup Guide](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/setup.md)
- [Anima MCP Tools Reference](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/mcp-tools.md)
- [Anima MCP Documentation](https://docs.animaapp.com/docs/integrations/anima-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live application URLs or local code files through the Anima service; long-running create and publish operations require extended timeouts.]

## Skill Version(s):

1.2.0 (source: server release evidence; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
