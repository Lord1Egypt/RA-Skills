## Description:

Build apps with the Claude API or Anthropic SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to choose the right Claude API, Anthropic SDK, or Agent SDK surface and apply language-specific examples for Python, TypeScript, Java, Go, Ruby, C#, PHP, and cURL integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready Agent SDK examples may run unpinned third-party MCP code.

Mitigation: Pin MCP package versions and review MCP server behavior before using examples in trusted workflows.

Risk: Examples may pass database credentials or other sensitive API data into agent or MCP workflows.

Mitigation: Use least-privileged test credentials, avoid production DATABASE_URL values, and treat API, file-upload, image, memory, and conversation-history examples as transmitting or retaining data.

Risk: Examples may bypass approval prompts for shell commands and file writes.

Mitigation: Keep default approval prompts enabled and use bypassPermissions only in disposable sandboxes.

## Reference(s):

- [Claude API documentation sources](shared/live-sources.md)
- [Python Claude API guide](python/claude-api/README.md)
- [TypeScript Claude API guide](typescript/claude-api/README.md)
- [Claude API tool use concepts](shared/tool-use-concepts.md)
- [Claude model guidance](shared/models.md)
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/claude-api-cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with language-specific code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls, SDK setup steps, model-selection guidance, and security-sensitive example patterns requiring user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
