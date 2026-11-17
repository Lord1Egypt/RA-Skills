## Description:

Maintains per-conversation decision notes and a write-ahead log to help OpenClaw agents recover context without mixing conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richgoodson](https://clawhub.ai/user/richgoodson)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to preserve decisions, corrections, and constraints for each conversation and recover them after interruptions or compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation notes could retain sensitive information.

Mitigation: Keep credentials, financial identifiers, and unnecessary personal information out of session notes; use the stop or confirmed delete controls when needed.

Risk: Promoting conversation-specific notes to shared memory could expose them to other conversations.

Mitigation: Propose each promotion to the user and write only entries they approve.

## Reference(s):

- [Agent Session State on ClawHub](https://clawhub.ai/richgoodson/skills/agent-session-state)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown session notes and conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-conversation notes; shared-memory promotion requires user approval.]

## Skill Version(s):

2.4.0 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
