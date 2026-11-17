## Description:

Gamified Habits helps OpenClaw users build routines with habit check-ins, XP, levels, attributes, achievements, boss battles, and generated adventure diary entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to create habits, check in through CLI commands or natural-language triggers, and view RPG-style progress summaries. The skill is intended for personal habit tracking with local JSON storage and optional Markdown diary generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit history and generated diaries can contain personal routine data and are stored locally in plaintext.

Mitigation: Use the skill only in trusted user environments, protect the data directory with operating-system permissions, and avoid recording sensitive habits.

Risk: Existing user data is included in the package.

Mitigation: Remove bundled user records before release or installation and initialize new installs from default empty data.

Risk: Manual user selection through command-line flags or environment variables can bypass the claimed data isolation on shared systems.

Mitigation: Validate and constrain user identifiers, keep storage paths within the current account's data directory, and prevent ordinary users from selecting another user's records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanwan2qq/skills/gamified-habits)
- [README](artifact/README.md)
- [Product Requirements Document](artifact/PRD.md)
- [User Data README](artifact/data/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and Markdown diary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local JSON habit data and Markdown diary entries under the skill data directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
