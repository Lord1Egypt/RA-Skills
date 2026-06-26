## Description: <br>
Analyzes one public fund from a natural-language question and returns a structured Markdown diagnostic report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for broad, single-fund diagnosis questions such as whether a fund is suitable to hold, how risky it is, or how its performance and holdings look. It is intended for one fund at a time and not for backtesting, portfolio optimization, data export, or multi-fund comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EastMoney API key and sends fund questions to EastMoney for analysis. <br>
Mitigation: Install only if the EastMoney service is trusted, keep EM_API_KEY revocable, and avoid including account numbers, personal identifiers, or full portfolio details in queries. <br>
Risk: Generated fund reports may be saved locally by default. <br>
Mitigation: Use --no-save when local Markdown report files should not be retained. <br>


## Reference(s): <br>
- [ClawHub fund-diagnosis release page](https://clawhub.ai/financial-ai-analyst/fund-diagnosis) <br>
- [Financial AI Analyst publisher profile](https://clawhub.ai/user/financial-ai-analyst) <br>
- [EastMoney MiaoXiang service](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional local Markdown file output and concise error text when the service fails.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and sends a single natural-language fund question to EastMoney for analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
