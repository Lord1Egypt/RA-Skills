## Description:

Scenario-focused Sparki skill for editing vlog-style videos while using the latest official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn local vlog, travel, daily-life, and lifestyle video footage into creator-style edits through Sparki's cloud workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files and prompts are sent to Sparki cloud processing.

Mitigation: Use the skill only for footage and prompts that are acceptable to process through Sparki, and use local tools when privacy or offline processing is required.

Risk: The setup command can store the Sparki API key in local plaintext configuration.

Mitigation: Prefer providing SPARKI_API_KEY through the environment instead of saving the key with setup.

Risk: The workflow uploads the local file path selected by the agent or user.

Mitigation: Confirm the exact video path before upload.

## Reference(s):

- [AI Vlog Editor on ClawHub](https://clawhub.ai/fischerlam/skills/ai-vlog-editor)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Sparki setup, upload, edit, polling, and download guidance; the CLI can return task IDs, status, result URLs, and downloaded video files.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, release metadata, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
