## Description:

Create, build, and modify Cocos 2D/3D game projects using the Cocos CLI and Cocos MCP server instead of manual scene or engine-file edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyihunter](https://clawhub.ai/user/liuyihunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game engineers use this skill to create Cocos projects, modify game scenes and components through the Cocos MCP server, and build web-targeted test packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may start and automatically register a long-running local MCP server without approval.

Mitigation: Require explicit confirmation before MCP registration, keep the server local, and shut it down after the work is complete.

Risk: Unsafe command construction could affect generated project paths or Cocos CLI invocations.

Mitigation: Validate project names with a strict allowlist and review Cocos CLI commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuyihunter/skills/cocos-cli-game-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify Cocos project files and may start a local Cocos MCP server.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
