## Description:

Captures learnings, errors, corrections, and feature requests in markdown files so agents can improve future workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suncrespo](https://clawhub.ai/user/suncrespo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record corrections, command failures, feature requests, and durable workflow lessons in project-local learning files. It also provides optional hook and OpenClaw guidance for reminding agents to capture useful learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files and promoted memory can carry unreviewed or sensitive content into future agent context.

Mitigation: Keep learning logs project-local, review entries before promotion, and store only concise sanitized summaries with no secrets or raw transcripts.

Risk: Broad or user-level hooks can add learning reminders across many prompts and workspaces.

Mitigation: Use opt-in, project-level hook configuration and avoid global hooks unless persistent coverage is explicitly desired.

Risk: Cross-session sharing can expose transcript excerpts, command output, or workspace details.

Mitigation: Use cross-session tools only in trusted environments and share short sanitized summaries with relevant paths instead of raw transcript content.

## Reference(s):

- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured log-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or recommends project-local .learnings markdown files when the agent follows the skill.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
