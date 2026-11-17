## Description:

Context Brief helps OpenClaw agents preserve and restore short, user-directed context anchors across sessions by reading local memory files and writing only to memory/anchors/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to checkpoint active work, decisions, pending items, and key paths before conversation compaction or when resuming after time away. It is intended for user-initiated context notes and anchor files, not automatic logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anchor files may preserve sensitive workspace context if the user asks the agent to save private details.

Mitigation: Avoid asking the skill to save secrets or confidential details; review anchors under memory/anchors/ when working in private projects.

Risk: Saved context could become stale and mislead later work after project decisions change.

Mitigation: Treat restored anchors as a concise checkpoint and confirm important decisions against current project files before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tommot2/skills/context-brief)
- [Context Brief Homepage](https://clawhub.ai/skills/context-brief)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown notes and brief natural-language status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anchor files are capped at 20 lines and written only to memory/anchors/ when requested or consented.]

## Skill Version(s):

3.0.0 (source: server release metadata, target metadata, SKILL.md H1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
