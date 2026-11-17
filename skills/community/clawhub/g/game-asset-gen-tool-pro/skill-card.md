## Description:

游戏资产生成-专业版 helps agents draft game assets, GDDs, style guides, batch asset plans, GLB-oriented 3D model prompts, and engine-compatible configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers, designers, and agent users use this skill to generate structured game asset prompts, 2D/3D asset specifications, batch asset plans, game design documents, and style-consistency guidance for game production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, and command permissions can affect files or execute actions beyond simple asset drafting.

Mitigation: Use the skill in a dedicated project workspace and review generated commands before execution.

Risk: Network and callback behavior is underdefined, including optional callback_url use.

Mitigation: Use callback_url only for endpoints you control and avoid providing secrets unless the agent explains the need.

Risk: Generated game assets, code examples, and design documents may require creative, technical, or licensing review before production use.

Mitigation: Have a human reviewer validate asset quality, engine compatibility, licensing assumptions, and project-specific design choices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/game-asset-gen-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, text, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include asset prompts, GLB-oriented specifications, GDD sections, batch plans, execution logs, and command proposals for user review.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
