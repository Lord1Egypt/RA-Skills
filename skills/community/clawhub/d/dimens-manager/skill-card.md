## Description:

Guides agents through Dimens/BintelAI business administration tasks for authentication, team and project context, tables, permissions, workflows, reports, and canvases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyowl](https://clawhub.ai/user/flyowl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer Dimens/BintelAI project resources with guided command sequences and checks. It supports resource creation, configuration, maintenance, and troubleshooting across authentication, teams, projects, tables, permissions, workflows, reports, and canvases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live administrative actions affecting Dimens/BintelAI credentials, permissions, publishing, rollback, and deletion workflows.

Mitigation: Require explicit user confirmation before deletes, restores, public sharing, permission changes, and API key lifecycle actions.

Risk: Authentication secrets, access tokens, or local CLI profiles could be exposed during operational troubleshooting.

Mitigation: Use only the official trusted base URL for authentication, avoid placing real secrets in chats or command lines, and protect or clear CLI profiles that store tokens.

Risk: Incorrect team, project, or resource context can cause commands to affect the wrong tenant or asset.

Mitigation: Confirm authentication, teamId, projectId, and resource ownership before writes, and read the current resource state before submitting updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyowl/skills/dimens-manager)
- [Dimens/BintelAI product site](https://dimens.bintelai.com/)
- [Skill definition](artifact/SKILL.md)
- [Skill README](artifact/README.md)
- [Key authentication overview](artifact/references/key-auth/overview.md)
- [Team context overview](artifact/references/team/overview.md)
- [Project initialization overview](artifact/references/project/overview.md)
- [Table management overview](artifact/references/table/overview.md)
- [Permission management overview](artifact/references/permission/overview.md)
- [Workflow overview](artifact/references/workflow/overview.md)
- [Report overview](artifact/references/report/overview.md)
- [Canvas overview](artifact/references/canvas/overview.md)
- [Approval workflow generation](artifact/references/workflow/references/approval-generation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Dimens CLI command sequences, validation checks, and read-before-write workflow steps.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
