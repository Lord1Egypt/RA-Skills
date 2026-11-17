## Description:

Figma设计集成-专业版 helps agents manage Figma workspaces for component library management, design variable extraction, batch export, comment management, and team collaboration workflow automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and enterprise teams use this skill to inspect Figma design systems, extract components and design variables, batch-export assets, and manage team review comments through agent-guided workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording could lead the agent to use the skill outside explicit Figma design tasks.

Mitigation: Limit use to clear Figma workspace, design system, asset export, or design review requests.

Risk: Comment posting, replies, and deletion can affect shared team files.

Mitigation: Require explicit user approval before posting, replying to, or deleting comments in shared Figma files.

Risk: The MorphixAI API key can expose account access if mishandled.

Mitigation: Keep the key in a scoped, revocable environment variable and avoid storing it in prompts, code, logs, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/figma-design-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with text, JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured result objects with status, data, execution log, and error fields.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
