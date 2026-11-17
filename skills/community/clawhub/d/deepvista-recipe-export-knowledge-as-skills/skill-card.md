## Description:

Recipe: Export Recipes as installable SKILL.md files for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to export DeepVista recipes as installable SKILL.md files for AI agents such as Claude Code, Cursor, and OpenCode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deepvista-cli dependency is not pinned in the skill metadata.

Mitigation: Install only from a trusted DeepVista package source and verify the package before use.

Risk: Exported SKILL.md files can affect future agent behavior after installation.

Mitigation: Review and scan exported skills before adding them to an agent skills directory.

Risk: The workflow creates files in an agent skills directory when the user saves exported skills.

Mitigation: Confirm the destination path and generated content before making exported skills discoverable by an agent.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-recipe-export-knowledge-as-skills)
- [deepvista-recipe skill reference](../deepvista-recipe/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [Markdown with bash command blocks and generated SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the deepvista CLI and deepvista-recipe skill; exported SKILL.md files should be reviewed before installation.]

## Skill Version(s):

0.1.0-alpha.21 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
