## Description:

ClawBrain Memory gives OpenClaw agents long-term memory across conversations, with source-aware recall, identity updates, and transparent degradation when memory access is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users install this skill to help agents remember prior conversations, user preferences, important decisions, and profile changes across sessions. It is intended for long-running assistant workflows where source-aware memory recall and memory-management transparency are important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories may persist sensitive, personal, business, legal, medical, or confidential information across sessions.

Mitigation: Install only where persistent memory is appropriate, and confirm that users know how to inspect, correct, delete, disable, and control the memory store.

Risk: Automatically updated profile or identity facts may become stale, overbroad, or incorrect.

Mitigation: Review recalled identity facts during use and correct, archive, or remove outdated details when a user's role or preferences change.

Risk: The evidence does not describe clear consent limits or retention boundaries for stored memories.

Mitigation: Avoid using the skill for regulated or confidential topics unless retention, consent, deletion, and access-control expectations are documented and acceptable.

## Reference(s):

- [ClawBrain Memory on ClawHub](https://clawhub.ai/michaelfeng/skills/clawbrain-pro-memory)
- [ClawBrain Dashboard](https://clawbrain.dev/dashboard)
- [ClawBrain](https://clawbrain.dev)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recalled user statements, AI-generated summaries, memory-source labels, and memory-service availability notices.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
