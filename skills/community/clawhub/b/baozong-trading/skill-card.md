## Description: <br>
A Chinese-language stock analysis and trading-decision skill for A-share, Hong Kong, and U.S. market workflows including stock diagnosis, portfolio review, risk checks, stock selection, and backtesting support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and market analysts use this skill to structure stock research, portfolio risk reviews, pre-market opportunity scans, daily reviews, strategy backtests, and decision checklists. Its outputs are advisory analysis frameworks and should not be treated as automatic trading instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce buy, sell, stop-loss, portfolio, or position-sizing guidance that users could mistake for executable financial advice. <br>
Mitigation: Treat all outputs as advisory, require human review before decisions, and never allow the skill to place trades automatically. <br>
Risk: Market analysis can be incorrect when based on stale, incomplete, or unverified market data. <br>
Mitigation: Verify prices, fundamentals, news, and policy signals independently with trusted market data sources before relying on the analysis. <br>
Risk: Broad finance triggers may activate the skill during general market conversations. <br>
Mitigation: Review the skill's scope before deployment and keep brokerage credentials or trading-system access outside this skill unless handled by a separately trusted tool. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zmy1006-sudo/baozong-trading) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured Chinese-language analysis templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory finance outputs; quality depends on user-provided or externally verified market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
