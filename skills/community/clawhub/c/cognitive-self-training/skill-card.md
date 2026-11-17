## Description:

Daily cognitive training, dream review, dream-scene narration, and self-improvement loop for OpenClaw, Hermes, Codex, Claude Code, and other AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help an AI agent capture daily learning, run recall practice, consolidate mistakes and decisions, produce traceable dream-style reviews, and maintain project-local training memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps project-local training memory, which can retain summaries of user corrections, decisions, mistakes, preferences, and work patterns.

Mitigation: Use it only where local retention is acceptable, keep the store project-scoped and inspectable, and avoid sensitive conversations unless redacted summaries are acceptable.

Risk: Daily dream review automation can run recurring consolidation work on a schedule.

Mitigation: Confirm the schedule scope, write location, and pause or removal path before enabling automation; leave automation manual when the user has not consented to a schedule.

## Reference(s):

- [Automation And Scheduling](references/automation.md)
- [Dream Protocol](references/dream-protocol.md)
- [Dream Styles](references/dream-styles.md)
- [Cognitive Training Storage Schema](references/storage-schema.md)
- [Cognitive Training Templates](references/templates.md)
- [Training Protocols](references/training-protocols.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and project-local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local .cognitive-training files for cards, daily reviews, dream reviews, schedules, strategies, and concept links.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
