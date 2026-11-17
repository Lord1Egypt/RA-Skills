## Description:

Give an agent a persistent body-emotion state system that converts structured AnalysisInput JSON into runtime prompt tags and workspace state updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askkumptenchen](https://clawhub.ai/user/askkumptenchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local persistent body-emotion state, session bootstrap payloads, and turn-by-turn reply-shaping fields to an agent while verifying that the local bes CLI runtime is ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the package without pinning or review may introduce unexpected local runtime behavior.

Mitigation: Use a dedicated virtual environment, review or pin the body-emotion-sensor package version, and require user approval before installation.

Risk: The skill can persist emotion state, history, and language preferences in local workspace and user configuration files.

Mitigation: Disclose the local storage locations, keep workspace and agent identifiers stable and intentional, and require explicit confirmation before commands that change persistent preferences.

Risk: An agent may overstate runtime availability if the bes CLI is missing or not initialized.

Mitigation: Check that bes is installed and only treat the runtime as ready when bes check-init returns ready true.

## Reference(s):

- [Body Emotion Sensor ClawHub Skill Page](https://clawhub.ai/askkumptenchen/skills/body-emotion-sensor)
- [Publisher Profile](https://clawhub.ai/user/askkumptenchen)
- [Package source repository referenced by the skill](https://github.com/AskKumptenchen/body-emotion-sensor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON field names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe workspace-specific CLI commands, local state paths, and runtime fields such as TURN_CHANGE_TAGS, BODY_TAG, and BASELINE_PERSONA.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
