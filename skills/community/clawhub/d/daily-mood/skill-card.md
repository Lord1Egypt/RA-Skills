## Description:

Daily Mood generates mood-aware morning, evening, and immediate life-message prompts for registered users in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to register mood preferences, generate immediate mood-matched messages, and schedule daily morning and evening emotional-support prompts. It is not a mental-health diagnostic or therapy tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores mood and profile data that can reveal sensitive emotional state.

Mitigation: Use only where users explicitly opt in, keep stored profile data minimal, and restrict access to local user data files.

Risk: The authoritative security evidence reports unsafe local file access and persistence boundaries, including the --show path validation path.

Mitigation: Fix --show path validation before multi-user use and avoid exposing CLI arguments to untrusted users.

Risk: Scheduled morning and evening messages can continue after registration if user intent changes.

Mitigation: Require clear opt-in for scheduled pushes and honor per-user push-toggle state before sending messages.

## Reference(s):

- [Daily Mood ClawHub page](https://clawhub.ai/cosmofang/skills/daily-mood)
- [Cosmofang publisher profile](https://clawhub.ai/user/cosmofang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text prompts with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mood-specific prompts and local profile records for scheduled push workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
