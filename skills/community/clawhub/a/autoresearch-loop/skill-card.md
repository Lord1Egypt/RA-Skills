## Description:

Run an explicit, bounded modify-verify-decide loop toward a measurable metric with approval gates, scoped edits, and rollback proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run bounded, measurable improvement loops in version-controlled workspaces. It helps structure iterative code, configuration, or research-quality work around approved metrics, guard commands, scoped edits, rollback, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The loop may make unwanted edits if the goal, metric, commands, or scope are vague.

Mitigation: Require an explicit run contract before edits begin, including allowed paths, forbidden paths, verification, guard command, rollback strategy, and iteration cap.

Risk: A metric improvement may introduce regressions elsewhere in the project.

Mitigation: Run a separate approved guard command after each verify command and discard or rework changes when the guard fails.

Risk: Unattended execution, external research, or broad rollback actions may expose private data or disturb unrelated work.

Mitigation: Default to foreground operation, require explicit approval for background mode or external research, keep edits scoped, and revert only current-loop changes.

## Reference(s):

- [Loop Protocol](artifact/references/loop-protocol.md)
- [Pivot Protocol](artifact/references/pivot-protocol.md)
- [Lessons Protocol](artifact/references/lessons-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command summaries and optional code or configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single iteration stream with run-contract prompts, results logs, keep/discard decisions, and lesson summaries.]

## Skill Version(s):

0.2.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
