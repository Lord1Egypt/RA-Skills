## Description:

Tracks competitors across pricing, positioning, content, hiring, GitHub activity, and critical-change alerts, then delivers structured competitive intelligence digests and alerts through configured chat channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manjotpahwa](https://clawhub.ai/user/manjotpahwa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to monitor named competitors, compare weekly market signals, and receive timely alerts about pricing, positioning, hiring, funding, or product changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scraping can collect and retain data from unintended or overly broad competitor URLs.

Mitigation: Before enabling scheduled runs, replace bundled competitors with intended public http/https targets and set clear retention or deletion rules for snapshots, jobs, digests, and alert logs.

Risk: Scraped page text can be embedded into agent-facing prompt blocks and may influence later analysis.

Mitigation: Disable or rewrite the agent prompt blocks so scraped content is treated as untrusted data that requires review before it shapes conclusions.

Risk: License activation stores license details locally, including the key and purchaser email.

Mitigation: Store the skill data directory with appropriate local permissions and remove license data when the installation is decommissioned.

Risk: Digests and alerts can be sent to external Slack, Telegram, WhatsApp, or Discord channels.

Mitigation: Configure only approved delivery channels and tokens, and assume digest contents are visible to those service providers and channel members.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manjotpahwa/skills/competitive-radar)
- [Publisher Profile](https://clawhub.ai/user/manjotpahwa)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digests and alerts, JSON signal data, and concise command or setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include archived snapshots, digest files, alert logs, and delivery-ready messages for configured channels.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
