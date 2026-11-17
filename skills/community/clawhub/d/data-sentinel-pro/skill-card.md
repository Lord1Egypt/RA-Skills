## Description:

Data Sentinel Pro monitors authorized webpages, product prices, and competitor pages and alerts users when content changes are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anson125chen](https://clawhub.ai/user/anson125chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor webpages they are authorized to access for price, content, or status changes and to receive alert output through manual runs, Telegram, or email configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the host environment.

Mitigation: Monitor only URLs you are authorized to access, and avoid internal, localhost, metadata, authenticated, or otherwise sensitive URLs.

Risk: Cron examples can repeat checks automatically without strong destination controls.

Mitigation: Review each cron entry, target URL, and frequency before enabling it, and keep recurring checks intentional and removable.

Risk: Telegram or email alerts may send monitored URLs and detected change details to external providers.

Mitigation: Enable those alert channels only when sharing that information with the provider is acceptable, and keep credentials in local configuration or environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anson125chen/skills/data-sentinel-pro)
- [Publisher profile](https://clawhub.ai/user/anson125chen)
- [Project homepage listed in package metadata](https://asmartglobal.com)
- [Repository listed in package metadata](https://github.com/anson125chen/data-sentinel-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON configuration examples, and local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alert messages may include monitored URLs and detected change details; local state is stored under the user's OpenClaw data directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
