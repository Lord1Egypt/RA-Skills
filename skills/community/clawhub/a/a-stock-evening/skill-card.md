## Description:

A Stock Evening generates and optionally sends a daily A-share market closing report with index performance, market breadth, sector fund flows, hot sectors, turnover, and trading suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrislzg](https://clawhub.ai/user/chrislzg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to generate an end-of-day A-share market report after the China market close and optionally deliver it through Feishu on a weekday schedule.

### Deployment Geography for Use:

Global, with content focused on China A-share markets and Asia/Shanghai scheduling.

## Known Risks and Mitigations:

Risk: The send path uses an unsafe shell command and always sends to a hard-coded Feishu recipient.

Mitigation: Review before installing; do not enable --send or the documented cron job until the recipient is configurable and the shell command is replaced with an argument-array call such as execFile or spawn.

Risk: Recurring delivery can send automated market reports to an unintended Feishu destination.

Mitigation: Confirm where Feishu messages go before enabling recurring delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrislzg/skills/a-stock-evening)
- [ClawHub Publisher Profile](https://clawhub.ai/user/chrislzg)
- [Eastmoney Quote API](https://push2.eastmoney.com/api/qt/ulist.np/get)
- [Eastmoney Sector Funds API](https://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally send the generated report through the OpenClaw Feishu channel when invoked with --send.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
