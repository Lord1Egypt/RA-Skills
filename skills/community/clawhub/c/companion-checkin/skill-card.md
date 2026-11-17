## Description:

Run warm, adaptive personal check-ins for habits, mood, sleep, meals, focus, and daily progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqizzo](https://clawhub.ai/user/sqizzo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run daily wellness and habit check-ins, log personal responses, and generate short recap summaries from repeated entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save mood, sleep, meals, stress, and freeform wellness notes in a local plaintext JSONL file.

Mitigation: Treat data/checkins.jsonl as private, avoid shared machines unless file permissions are restricted, and delete or protect the log when history should not be retained.

Risk: Check-in recaps depend on self-reported local history and may reflect incomplete or stale entries.

Mitigation: Use recaps as lightweight personal summaries, and review the underlying entries before relying on patterns or trends.

## Reference(s):

- [Companion Check-In Data Schema](references/data-schema.md)
- [ClawHub skill page](https://clawhub.ai/sqizzo/skills/companion-checkin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from helper commands plus human-facing check-in prompts and recap prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads local JSONL check-in history at data/checkins.jsonl when logging or summarizing.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
