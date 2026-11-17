## Description:

Search and fetch ClawDocx guides, posts, prompts, skills and SOUL files for OpenClaw and Claude Code setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdocx](https://clawhub.ai/user/clawdocx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find ClawDocx documentation and library content for installing, configuring, securing, or running OpenClaw and Claude Code workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to ClawDocx's remote MCP server and may use a ClawDocx API key when configured.

Mitigation: Use OpenClaw's supported secret mechanism, keep the key out of chat transcripts, and avoid storing it as a literal in configuration.

Risk: Fetched prompts, skills, guides, or SOUL files could be reused without sufficient review.

Mitigation: Review fetched content before reuse and confirm before pasting prompt bodies into public channels.

## Reference(s):

- [ClawDocx agent setup](https://clawdocx.com/agents)
- [OpenClaw MCP tools documentation](https://docs.openclaw.ai/tools/mcp)
- [OpenClaw gateway configuration extensions](https://docs.openclaw.ai/gateway/config-extensions)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw skill creation documentation](https://docs.openclaw.ai/tools/creating-skills)
- [ClawHub skill format documentation](https://docs.openclaw.ai/clawhub/skill-format)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with URLs, configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cite ClawDocx result URLs and may describe optional API-key setup for member-only content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
