## Description:

Auto Skill Loader helps an agent discover local OpenClaw skills, classify them by protection level, and select candidate skills for task-driven loading or routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqleslie](https://clawhub.ai/user/zqleslie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep skill loading lightweight by scanning available skills, filtering core and protected skills, and surfacing dynamic candidates for task matching. It is suited to OpenClaw environments where automatic skill discovery and optional agent routing are part of the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically load and follow other local skill instructions with broad task triggers and limited user confirmation.

Mitigation: Install only where local skill directories are trusted and require explicit confirmation before loading newly discovered or changed skills.

Risk: Automatic routing can forward tasks in environments where routing is enabled.

Mitigation: Disable routing unless needed and review routing behavior before deployment.

Risk: Using a floating installer version can reduce release assurance.

Mitigation: Use a pinned installer version instead of @latest for higher assurance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zqleslie/skills/auto-skill-loader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands, configuration examples, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May list loadable, protected, and core skills; dry-run and JSON modes are available through the bundled Node.js script.]

## Skill Version(s):

2.0.1 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
