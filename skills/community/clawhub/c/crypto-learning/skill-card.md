## Description:

Crypto Learning provides a Chinese-language cryptocurrency self-study plan with daily lesson generation, progress tracking, skip and reset commands, and manual topic lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmzo](https://clawhub.ai/user/hmzo)

### License/Terms of Use:


## Use Case:

External learners and agent users use this skill to follow a structured cryptocurrency curriculum, receive beginner-friendly daily learning reports, and track learning progress across beginner, investment, and advanced-investment stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate automatic fresh-content behavior and scheduled delivery.

Mitigation: Confirm the host agent will register and run the daily schedule before relying on automated lessons.

Risk: Static cryptocurrency lessons may be mistaken for current financial information.

Mitigation: Treat generated lessons as educational material and verify market-sensitive claims against current authoritative sources.

Risk: The scheduled helper writes lesson content to a fixed /tmp path.

Mitigation: Run scheduled tasks under an unprivileged account and replace the fixed output path with a secure temporary file or private handoff directory.

Risk: Reset behavior clears saved progress.

Mitigation: Back up progress data before resetting or reinstalling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmzo/skills/crypto-learning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text learning reports with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily lesson output is intended to include explanations, current-source synthesis, examples, summaries, self-test questions, and progress updates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
