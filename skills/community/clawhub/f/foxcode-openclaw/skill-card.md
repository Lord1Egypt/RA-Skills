## Description:

Configure and manage Foxcode AI models in OpenClaw with guided API setup, endpoint selection, model configuration, validation, and status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to configure Foxcode Claude Code endpoints, store authentication profiles, choose primary and fallback models, validate setup, and monitor endpoint status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator may send a Foxcode API token to the configured baseUrl, including a custom or untrusted URL.

Mitigation: Review the configured baseUrl before running validation, use only trusted Foxcode endpoints, and rotate the token if it may have been sent to an untrusted URL.

Risk: The setup wizard writes OpenClaw configuration and auth-profiles files and may overwrite existing settings without creating its own backup.

Mitigation: Back up ~/.openclaw/openclaw.json and ~/.openclaw/agents/main/agent/auth-profiles.json before running the wizard, review generated changes before confirming, and keep rollback steps available.

## Reference(s):

- [Foxcode Endpoints Reference](references/foxcode-endpoints.md)
- [OpenClaw Configuration Reference](references/openclaw-config.md)
- [Foxcode Status Page](https://status.rjj.cc/status/foxcode)
- [Foxcode API Keys](https://foxcode.rjj.cc/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/clarezoe/skills/foxcode-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide users to run bundled Python scripts that modify OpenClaw configuration and authentication profile files.]

## Skill Version(s):

1.2.6 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
