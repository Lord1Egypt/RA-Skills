## Description:

Auto-compress session memories when context usage exceeds 85%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this hook to reduce retained session-memory context by compressing older daily memory logs into MEMORY.md after context usage crosses the configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook can automatically rewrite MEMORY.md and delete older memory files.

Mitigation: Enable it only with explicit opt-in or dry-run behavior, and require validated backups or archive-before-delete before cleanup.

Risk: The hook can create broad Git commits for local workspace changes.

Mitigation: Use path-limited Git staging, require review before committing, and avoid automatic push unless deliberately configured.

Risk: Shell-based Git execution and unclear trigger documentation can surprise users or expand the effect of the hook.

Mitigation: Use safe non-shell Git execution and document the exact events, threshold, file paths, and side effects before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/context-shrink)
- [Publisher profile](https://clawhub.ai/user/bg1avd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Text and Markdown status messages, MEMORY.md updates, memory file deletions, and Git commit commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as an OpenClaw hook and can modify local memory files when enabled.]

## Skill Version(s):

1.0.2 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
