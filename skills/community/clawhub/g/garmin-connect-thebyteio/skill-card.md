## Description:

Integrate with Garmin Connect to fetch and analyze deep fitness metrics including sleep, body battery, resting heart rate, stress, and training status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vegasbrianc](https://clawhub.ai/user/vegasbrianc)

### License/Terms of Use:


## Use Case:

Agents supporting Garmin Connect users use this skill to retrieve daily fitness and recovery metrics and turn them into training-readiness summaries or recovery-aware workout guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin credentials and personal health data.

Mitigation: Review before installing and use a dedicated low-privilege 1Password item or vault.

Risk: The login script passes credentials through heredoc-generated Python code.

Mitigation: Avoid running the login script until credential handling is fixed.

Risk: Session tokens and cached health metrics may be written to shared or default local paths.

Mitigation: Use a private 0700 session directory and set explicit cache permissions and retention.

Risk: Dependency installation may use system Python or unpinned packages.

Mitigation: Install dependencies in a pinned virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vegasbrianc/skills/garmin-connect-thebyteio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON data from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Garmin Connect data through helper scripts and may include local cache files for daily metrics.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
