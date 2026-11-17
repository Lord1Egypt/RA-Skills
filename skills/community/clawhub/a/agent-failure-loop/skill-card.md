## Description:

An end-to-end self-improvement loop that automatically detects agent failures, classifies them, tracks recurrence, auto-generates rules, and promotes them to AGENTS.md/CLAUDE.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record recurring agent failures, analyze repeated patterns, and promote reviewed lessons into persistent agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically and repeatedly change persistent agent instruction files using unvalidated failure-log content.

Mitigation: Run promotion in dry-run mode, inspect diffs manually, and restrict targets to project-owned instruction files.

Risk: Failure logs may contain secrets, personal data, proprietary paths, or confidential prompts.

Mitigation: Keep sensitive or confidential material out of failure records before syncing or sharing learnings.

Risk: Scheduled auto-promotion can apply low-quality or misleading rules without timely review.

Mitigation: Avoid scheduled auto-promotion unless a human review gate is in place.

## Reference(s):

- [Agent Failure Loop on ClawHub](https://clawhub.ai/reikys/skills/agent-failure-loop)
- [Publisher profile](https://clawhub.ai/user/reikys)
- [SKILL.md](artifact/SKILL.md)
- [sync-learnings.py](artifact/scripts/sync-learnings.py)
- [auto-promote.py](artifact/scripts/auto-promote.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON summaries, generated Markdown reports, configurable rules, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run modes and configurable failure, learning, target, format, and repeat-count settings.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
