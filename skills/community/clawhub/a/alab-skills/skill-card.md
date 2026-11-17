## Description:

Use as the top-level guide for ALab agent-facing role skills. It explains how to install the ALab CLI package, the root/project/experiment skill hierarchy, when to use each subskill, and how the three role skills differ without loading every command reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bebetterest](https://clawhub.ai/user/bebetterest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill bundle to choose the least-privileged ALab role skill, install the ALab CLI, and route root administration, project coordination, and experiment worktree tasks to the appropriate subskill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide root, project-admin, and worktree operations across ALab layers.

Mitigation: Keep credentials separated by layer and use the narrowest matching subskill for each task.

Risk: CLI installation and launcher command prefixes can affect what commands the agent runs.

Mitigation: Install ALab in an isolated environment, review or pin the alab-cli package where reproducibility matters, and only use launcher prefixes from trusted launchers.

Risk: Administrative cleanup, project submission, or lifecycle actions may be destructive or hard to reverse.

Mitigation: Confirm destructive admin actions and project submissions before running them.

## Reference(s):

- [ALab Skills on ClawHub](https://clawhub.ai/bebetterest/skills/alab-skills)
- [ALab Global Admin Commands](alab-global-admin/references/commands.md)
- [ALab Project Controller Commands](alab-project-controller/references/commands.md)
- [ALab Experiment Worker Commands](alab-experiment-worker/references/commands.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes English and Chinese skill and command-reference files.]

## Skill Version(s):

0.1.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
