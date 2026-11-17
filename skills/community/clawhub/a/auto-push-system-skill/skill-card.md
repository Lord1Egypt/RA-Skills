## Description:

Auto Push System Skill automates monitoring of AI-generated content and pushes podcast summaries, skill learning summaries, and conversation briefs to Feishu with logging and recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bianca1227](https://clawhub.ai/user/bianca1227)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure an automated workflow that detects AI-generated content readiness signals and sends selected content to Feishu. It is intended for recurring content notification workflows such as podcast summaries, skill learning summaries, and conversation briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default Feishu recipient and unchecked file paths can send unintended local files.

Mitigation: Replace the default chat ID, restrict processing to a dedicated trusted content directory, and require review before any external send.

Risk: Recurring cron jobs can repeatedly send content before the workflow is tested.

Mitigation: Disable recurring cron entries until configuration, Feishu authorization, and test content handling have been verified.

Risk: Running the workflow with broad local access can expose secrets or personal files.

Mitigation: Run with least-privilege permissions and avoid granting access to directories containing secrets or personal data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bianca1227/skills/auto-push-system-skill)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, scheduling, monitoring, and troubleshooting guidance for a Feishu content-push workflow.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
