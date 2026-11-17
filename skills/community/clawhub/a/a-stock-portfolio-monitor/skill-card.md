## Description:

A股持仓监控助手 helps monitor A-share positions, generate portfolio profit-and-loss reports, and run a rule-based stock selector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinesdff](https://clawhub.ai/user/sunshinesdff)

### License/Terms of Use:

MIT-0

## Use Case:

Personal investors and agents can use this skill to configure A-share holdings, produce local portfolio reports, and run a simple multi-factor screen over a fixed stock pool. The skill's own disclaimer states that outputs are for reference only and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interactive menu input can flow into shell execution and run unintended local commands.

Mitigation: Avoid the interactive menu with untrusted input; use direct, validated script calls only after shell execution is fixed.

Risk: Portfolio holdings are stored locally and may contain sensitive financial information.

Mitigation: Run the skill in a user-controlled environment and protect the local portfolio file with appropriate filesystem permissions.

Risk: The scripts contact Tencent Finance and use HTTP for some market data.

Mitigation: Use the skill only where outbound network access and the quote data source are acceptable, and verify market data before making financial decisions.

Risk: Automatic alerts are advertised but not implemented in the artifact behavior.

Mitigation: Treat the skill as a manual report and screening tool unless alerting is separately implemented and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshinesdff/skills/a-stock-portfolio-monitor)
- [Publisher profile](https://clawhub.ai/user/sunshinesdff)
- [Tencent Finance quote endpoint used by the scripts](http://qt.gtimg.cn/q={prefix}{code})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Chinese CLI text reports with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores portfolio holdings locally and fetches market quote data from Tencent Finance endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
