## Description:

Daily Producer creates personalized daily AI news reports by collecting multi-platform information from a user profile, filtering noise, generating structured summaries, and rendering HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ailab2026](https://clawhub.ai/user/ailab2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run a personalized daily AI news pipeline that collects sources, prepares candidates, has an agent generate a daily JSON briefing, renders HTML, and optionally sends a Feishu card notification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad credentials, including Feishu-related access.

Mitigation: Review the Feishu credential flow and grant only the permissions needed before installation.

Risk: The feedback server can create network-facing write access.

Mitigation: Disable the feedback server or bind it to localhost with authentication before use.

Risk: Security guidance reports a hard-coded proxy credential.

Mitigation: Remove the hard-coded proxy credential and require user-provided configuration.

Risk: Security guidance reports shell command construction that needs review.

Mitigation: Fix shell command construction and review command inputs before execution.

Risk: The skill uses telemetry and background services.

Mitigation: Make telemetry and background services explicit opt-in and document when they run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ailab2026/skills/daily-producer)
- [Pipeline overview](artifact/reference/pipeline/00_overview.md)
- [Daily collection guide](artifact/reference/daily_collection_guide.md)
- [JSON generation rules](artifact/reference/pipeline/06_generate_json.md)
- [Daily payload example](artifact/reference/daily_payload_example.json)
- [Profile template](artifact/reference/profile_template.yaml)
- [OpenCLI output formats](artifact/reference/opencli_output_formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON/HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes profile, raw collection, daily JSON, daily HTML, archive, feedback, and server log files when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
