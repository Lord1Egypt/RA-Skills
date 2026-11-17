## Description:

Scheduled intelligence research pipeline that monitors topics on a twice-daily cadence, produces signal-first digests, and maintains META.json freshness state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverho](https://clawhub.ai/user/riverho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run an OpenClaw-based research workflow that tracks configured topics, filters news into signals, updates per-topic freshness state, and prepares concise digests for Telegram or WhatsApp delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented curl-from-master install path can execute mutable remote code.

Mitigation: Install from a pinned and verified release instead of a moving branch archive.

Risk: The fresh install flow registers recurring OpenClaw cron jobs.

Mitigation: Inspect INSTALL/install.sh and SCRIPTS/setup-cron.sh, then approve scheduling only after confirming the jobs and cadence are acceptable.

Risk: The install script may modify the Python environment while installing PyYAML.

Mitigation: Use an isolated environment or preinstall reviewed dependencies before running the setup script.

Risk: Digests may be delivered through Telegram or WhatsApp.

Mitigation: Configure only delivery channels suitable for the sensitivity of the monitored topics and generated digests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/riverho/skills/attention-research)
- [Publisher Profile](https://clawhub.ai/user/riverho)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text digests with shell commands and YAML/JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic news files, META.json freshness state, cron job entries, and Telegram or WhatsApp-ready digest text.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
