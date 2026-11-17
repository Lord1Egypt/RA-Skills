## Description:

Sync encrypted Apple Health data from an iOS device (iPhone, iPad) to OpenClaw, Hermes Agent, Claude, Codex or any other AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukasosterheider](https://clawhub.ai/user/lukasosterheider)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to onboard an iOS device, fetch and locally decrypt Apple Health snapshots, unlink devices, and generate daily, weekly, or monthly health summaries for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Apple Health-derived data and private sync keys stored under the selected local state directory.

Mitigation: Keep the state directory private, do not share private keys, rotation backups, databases, NDJSON exports, or saved reports, and preserve the documented file permissions.

Risk: The sync workflow uses a disclosed Supabase relay for onboarding, fetching encrypted rows, and unlinking devices.

Mitigation: Use only the documented relay URLs and rely on local decryption; do not send private keys or health records to the onboarding relay.

Risk: Dependency installation, identity rotation, unlinking, report saving, and recurring schedules can affect sensitive local state or recurring access patterns.

Mitigation: Run those actions only after explicit user confirmation of the dependency install, unlink, rotation, report destination, or schedule.

## Reference(s):

- [Health Sync homepage](https://gethealthsync.app/)
- [Health Sync for OpenClaw iOS app](https://apps.apple.com/app/health-sync-for-openclaw/id6759522298)
- [ClawHub skill page](https://clawhub.ai/lukasosterheider/skills/apple-health-sync)
- [Config reference](references/config.md)
- [Default runtime config](references/configs.defaults.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus optional text or JSON health summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local private state, onboarding artifacts, encrypted-sync outputs, SQLite or NDJSON health snapshots, and confirmed saved summaries.]

## Skill Version(s):

0.9.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
