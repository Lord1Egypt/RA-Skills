## Description:

Automatically reads relevant project context before major actions, including TODO.md, roadmap.md, handoffs, task plans, and related files, so agents operate with situational awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to load prioritized project context before starting, implementing, refactoring, debugging, planning, resuming, or handing off work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands can fetch different content over time.

Mitigation: Install a pinned, reviewed ClawHub version or a specific commit, and review the install command before running it.

Risk: The skill automatically reads local project context files that may contain sensitive or unrelated private notes.

Mitigation: Keep secrets out of TODO.md, roadmap.md, task_plan.md, handoff files, findings, changelogs, and session summaries before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/auto-context)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown context summary with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stale-file warnings and missing-context notices based on local project files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
