## Description:

Automatically syncs and maintains detailed conversation logs and activity digests across agent sessions for persistent memory and context recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harvnk](https://clawhub.ai/user/harvnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve context across OpenClaw agent sessions by generating reusable conversation logs and activity digests. It is suited to environments where persistent transcript capture has been explicitly accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation logs can copy private agent transcripts into workspace Markdown files.

Mitigation: Use explicit per-agent or per-session opt-in, apply secret and personal-data redaction, and restrict file permissions.

Risk: Recurring cron jobs can continue collecting conversation data after users no longer expect capture.

Mitigation: Document and provide a clear way to disable the cron jobs, and apply retention limits for generated logs and digests.

Risk: Default startup loading can expose prior conversation content to every future agent session.

Mitigation: Limit startup loading to approved agents and sessions, and avoid enabling it in sensitive environments without review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harvnk/skills/conversation-memory-sync)
- [Publisher Profile](https://clawhub.ai/user/harvnk)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates persistent CONVERSATION_LOG.md and ACTIVITY_DIGEST.md files when used with the described scripts and cron setup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
