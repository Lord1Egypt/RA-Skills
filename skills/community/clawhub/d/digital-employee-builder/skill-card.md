## Description:

Builds a runnable agent digital employee from a business codebase, API documentation, or functional specification, including workspace files, MCP tooling, workflow skills, onboarding steps, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaggerxzj](https://clawhub.ai/user/jaggerxzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to convert a business capability into an agent workspace with identity, rules, tools, workflow skills, and onboarding instructions. It supports OpenClaw by default and can adapt outputs for Claude Code, Cursor, or custom harnesses when specified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workspaces can include live write-capable tools that use business credentials.

Mitigation: Review and harden the generated workspace before live use, require explicit approval gates, use least-privilege short-lived tokens, and test write-capable tools in a non-production environment first.

Risk: Unpinned dependencies or runtime package downloads can change behavior after installation.

Mitigation: Pin dependencies, avoid runtime package downloads, and verify generated scripts and MCP servers in a clean environment before deployment.

Risk: Generated memory, documentation, or setup files may capture sensitive business details.

Mitigation: Keep generated memory and workspace documentation out of public repositories, redact sensitive content, and store only credential variable names rather than secret values.

Risk: Scheduled heartbeat or always-on write-capable tools can perform unexpected actions if enabled too early.

Mitigation: Enable scheduled heartbeat and write-capable tools only after explicit approval, smoke testing, and confirmation that approval boundaries are documented in the workspace.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/jaggerxzj/digital-employee-builder/tree/main/skills/digital-employee-builder)
- [ClawHub skill page](https://clawhub.ai/jaggerxzj/skills/digital-employee-builder)
- [Business-Code Modification Proposals](artifact/references/business-api-proposals.md)
- [Harness Adapters: Onboarding Outside OpenClaw](artifact/references/harness-adapters.md)
- [MCP Wrapping Essentials](artifact/references/mcp-integration.md)
- [OpenClaw Workspace Specification](artifact/references/openclaw-workspace.md)
- [Script Encapsulation of Business Code](artifact/references/script-encapsulation.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown workspace files, generated skill files, MCP server code, setup snippets, and verification steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated MCP server and workflow scripts; write-capable business tools require explicit approval gates.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
