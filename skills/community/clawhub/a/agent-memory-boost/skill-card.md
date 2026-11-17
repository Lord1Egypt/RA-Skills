## Description:

Persistent task memory and keep-alive loop for OpenClaw agents. Every task gets durable notes. Arm the loop for long tasks, disarm when done. No external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techieter](https://clawhub.ai/user/techieter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to keep task state across sessions by creating durable RESUME, CHECKLIST, and DOCS notes for each task and optionally arming monitoring jobs for long-running work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes every task to persistent local files under ~/.openclaw/memory/.

Mitigation: Install only if persistent local task logging is acceptable, and delete stored notes when they are no longer needed.

Risk: The installer adds five recurring OpenClaw jobs, including always-on validator and smoke-test jobs.

Mitigation: Review install.sh before running it, skip or remove scheduled jobs if they are not needed, and remove the jobs during uninstall.

Risk: The documented ClawHub install command uses npx clawhub@latest.

Mitigation: Pin the ClawHub installer version before installation when reproducible installation behavior is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techieter/skills/agent-memory-boost)
- [Project homepage](https://github.com/TechieTer/openclaw-memory-boost)
- [OpenClaw and Obsidian variant](https://clawhub.ai/techieter/memory-keep-alive-for-obsidian)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, concise text status lines, and shell commands in installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task state under ~/.openclaw/memory/ and configures recurring OpenClaw jobs when installed.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
