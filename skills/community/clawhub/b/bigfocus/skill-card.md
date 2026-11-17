## Description:

BigFocus is a personal tracker that monitors product prices, celebrity or public figure updates, industry news, and custom metrics, then reports detected changes through scheduled checks and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use BigFocus to maintain personal watchlists for prices, people, industries, and metrics, with scheduled checks that report only detected changes. Operators can use the included cron template to run hourly scans and deliver updates through supported OpenClaw channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hourly scans can read and write workspace memory, perform web searches, fetch public product or API pages, and send update messages.

Mitigation: Install only when persistent tracking is expected, keep cron setup explicit, and review configured channels and targets before enabling delivery.

Risk: Automatic product scans can make unsafe user-controlled web requests.

Mitigation: Review or patch URL validation before enabling automatic product scans, and avoid tracking targets from untrusted sources.

Risk: Stored tracker data can be corrupted by unescaped tracker names, targets, or values.

Mitigation: Avoid adding untrusted tracker names, targets, or values until Markdown storage is hardened, and periodically review tracker entries.

## Reference(s):

- [BigFocus ClawHub release page](https://clawhub.ai/kobenfang/skills/bigfocus)
- [Cron install shell template](artifact/references/cron-install-shell.sh)
- [Cron templates JSON](artifact/references/cron-templates.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and confirmation prompts, JSON helper-command output, and shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled scans stay quiet when no changes are found; tracker state and raw data are stored in workspace memory files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
