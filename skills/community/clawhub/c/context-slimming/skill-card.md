## Description:

Diagnose and optimize an OpenClaw agent workspace's injected context files to reduce per-round token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scomper](https://clawhub.ai/user/scomper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent workspace maintainers use this skill to audit top-level OpenClaw context files, remove duplication, split detailed rules into on-demand references, and verify token reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to delete workspace context files while reducing injected context.

Mitigation: Require a proposed patch first, approve each deletion explicitly, keep backups or work on a clean Git branch, and review diffs before committing.

Risk: The documented workflow includes broad workspace staging with `git add -A`.

Mitigation: Stage only reviewed files and avoid broad staging commands when applying slimming changes.

Risk: Slimming context can remove guidance that agents still need for safe or correct behavior.

Mitigation: Keep detailed rules in on-demand references, restart the agent after changes, and verify expected behavior before relying on the slimmed context.

## Reference(s):

- [Context Slimming ClawHub Page](https://clawhub.ai/scomper/skills/context-slimming)
- [Publisher Profile](https://clawhub.ai/user/scomper)
- [Before/After Reference](references/before-after.md)
- [Slimming Checklist](references/checklist.md)
- [Wenyan Patterns](references/wenyan-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and file-layout examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace context-slimming guidance; proposed deletions and broad staging should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
