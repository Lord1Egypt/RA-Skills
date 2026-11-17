## Description:

Monitors China bank deposit, LPR, government bond, SHIBOR, mortgage, and open market operation rates and alerts when tracked values change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanbihai](https://clawhub.ai/user/ryanbihai)

### License/Terms of Use:

MIT-0

## Use Case:

Finance professionals, mortgage holders, investors, and economic researchers use this skill to monitor Chinese interest rate changes and receive concise change alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound requests to public finance and rate websites may fail or return incomplete, delayed, or inaccurate data.

Mitigation: Verify rate data against authoritative sources before using it for financial decisions.

Risk: Running the skill can update its local rates.json comparison state.

Mitigation: Review local state changes when auditing alerts, and narrow trigger phrases if accidental activation would be noisy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryanbihai/skills/chinese-interest-rate)
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/)
- [SHIBOR](https://www.shibor.org/shibor/web-htmls/shibor.html)
- [ChinaMoney SHIBOR Endpoint](https://www.chinamoney.com.cn/ags/ms/cm-u-bond-shibor/Shibor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Plain text notifications with markdown-style sections and JSON-backed local state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates local rates.json after comparing fetched or agent-supplied rates; remains quiet when no tracked rates change.]

## Skill Version(s):

3.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
