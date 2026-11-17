## Description:

Aky Select runs a command-line screener for China A-share stocks using nine price, liquidity, trend, relative-strength, VWAP, and capital-flow filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, analysts, and developers use this skill to run a command-line A-share stock screener after market close or on demand. It narrows candidates using technical and market-flow filters and should be treated as screening support, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron setup creates persistent unattended execution under the user's account.

Mitigation: Prefer the one-time Python command; if scheduled mode is enabled, review the crontab command, track the entry, avoid duplicate entries, and account for future script or dependency changes.

Risk: Stock-screening results can be mistaken for investment recommendations.

Mitigation: Use the output only as technical screening information and apply independent review before making trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangfromchu-ai/skills/aky-select)
- [Project homepage](https://github.com/aky/aky-select)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text console tables and progress output, with Markdown shell-command examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and the akshare package; optional cron usage schedules unattended runs.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
