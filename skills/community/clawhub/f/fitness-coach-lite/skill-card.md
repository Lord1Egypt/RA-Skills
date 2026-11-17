## Description:

Fitness Coach Lite is a Telegram-native personal workout tracker for low-friction workout logging, status tracking, adaptive training suggestions, and daily, weekly, and monthly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhan2021](https://clawhub.ai/user/youhan2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal fitness agents use this skill to capture workout, status, body, and plan updates from short chat-style messages, then generate daily, weekly, monthly, and summary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture and persist sensitive workout, body, sleep, menstrual, injury, and free-form note data in local files.

Mitigation: Use explicit commands, review generated records, and protect or periodically delete the data directory on shared machines or backups.

Risk: Workout plans can be imported from local file paths.

Mitigation: Import plans only from trusted paths and inspect plan JSON before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses with JSON-backed local records and shell commands for the bundled workout CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workout, status, plan, session, and body-status records under the skill data directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
