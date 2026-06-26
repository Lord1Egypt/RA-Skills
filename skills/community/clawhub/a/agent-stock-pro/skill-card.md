## Description: <br>
Agent Stock Pro helps agents screen stocks, produce short-term trading decisions, analyze holdings, generate PDF reports, and simulate strategy tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tompchen](https://clawhub.ai/user/tompchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for stock screening, single-stock trading analysis, holdings review, quant scoring, PDF report generation, and simulated portfolio tracking for short-term market decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist simulated portfolio data and generated financial analysis under dist/. <br>
Mitigation: Run it in a dedicated workspace and review generated or modified files before enabling recurring automation. <br>
Risk: Generated PDF reports may be sent through the configured message or WeChat channel without clear per-run approval. <br>
Mitigation: Require manual confirmation before outbound report delivery and review reports before sending them to users. <br>
Risk: The workflow may install Python packages needed for stock analysis and PDF generation. <br>
Mitigation: Install dependencies only in an isolated environment and confirm package installation commands before execution. <br>


## Reference(s): <br>
- [Agent Stock Pro on ClawHub](https://clawhub.ai/tompchen/agent-stock-pro) <br>
- [Original Agent Stock skill](https://clawhub.ai/anoyix/agent-stock) <br>
- [Screening workflow](references/screen.md) <br>
- [Trade decision workflow](references/trade.md) <br>
- [Quant decision workflow](references/quant.md) <br>
- [Quant scoring rules](references/quant_rule.md) <br>
- [Holdings analysis workflow](references/holdings.md) <br>
- [Strategy tracking workflow](references/strategy-track.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports, JSON portfolio state, PDF reports, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis reports under dist/, update simulated portfolio history, and prepare generated PDF reports for delivery.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
