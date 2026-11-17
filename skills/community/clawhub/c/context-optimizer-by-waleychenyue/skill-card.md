## Description:

The context optimizer analyzes, trims, and rewrites OpenClaw workspace context files, then extracts reusable workflows into standalone skills to reduce token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waleychenyue](https://clawhub.ai/user/waleychenyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace maintainers use this skill to audit context size, generate optimization reports, apply selected reductions, and package reusable context workflows as skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and may rewrite sensitive OpenClaw context files, including memory, identity, user, and tool files.

Mitigation: Run read-only analysis first, use backups, inspect diffs, and apply changes only in workspaces where exposing those files to the optimizer process is acceptable.

Risk: Automated scheduled optimization or CI auto-commit workflows can persist changes with weak review boundaries.

Mitigation: Do not enable weekly cron jobs or CI auto-commit flows unless scoped paths, approval gates, and human review are added.

Risk: Rewritten context or extracted skills may remove important instructions or change agent behavior.

Mitigation: Prefer conservative or balanced optimization, review generated skills before use, and keep rollback paths available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waleychenyue/skills/context-optimizer-by-waleychenyue)
- [EXAMPLES.md](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write analysis reports, JSON data, optimized context files, or extracted SKILL.md files in an OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
