## Description: <br>
Helps developers build apps with the Claude API, Anthropic SDKs, and Agent SDK using language-specific guidance and examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose the right Claude API, tool-use, or Agent SDK surface and implement Claude integrations across Python, TypeScript, Java, Go, Ruby, C#, PHP, or raw HTTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied examples may involve file uploads, tool execution, memory, or automatic code edits. <br>
Mitigation: Review examples before use, avoid sending secrets or regulated files unless approved, scope tool permissions and working directories, and add review gates before file deletion, code execution, or automatic edits. <br>
Risk: Cached model names, pricing, and API capabilities may become outdated. <br>
Mitigation: Verify current model, pricing, and capability details against the live Claude documentation links before using the guidance in production. <br>
Risk: Agent SDK or MCP integrations can broaden access to files, terminals, or external services. <br>
Mitigation: Use trusted MCP endpoints only, prefer default permissions, and limit agent tools to the minimum access needed for the task. <br>


## Reference(s): <br>
- [Claude API live documentation sources](shared/live-sources.md) <br>
- [Claude model reference](shared/models.md) <br>
- [Claude tool-use concepts](shared/tool-use-concepts.md) <br>
- [Python Claude API guide](python/claude-api/README.md) <br>
- [TypeScript Claude API guide](typescript/claude-api/README.md) <br>
- [Claude API models overview](https://platform.claude.com/docs/en/about-claude/models/overview.md) <br>
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include language-specific SDK examples, API parameters, error-handling guidance, and documentation links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
