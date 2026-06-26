## Description: <br>
股票全面分析 v2.1 provides HK, US, and A-share quote lookup, technical indicators, analyst ratings, and a seven-section stock analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate stock quote summaries, technical analysis, analyst-rating context, and action-oriented stock reports for HK, US, and A-share symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports hardcoded API credentials and possible token exposure. <br>
Mitigation: Rotate or remove embedded credentials before use, keep service tokens in environment variables, and restrict access to least privilege. <br>
Risk: The security review warns that simulated technical indicators may be presented as normal financial analysis. <br>
Mitigation: Remove simulated-data paths or label them clearly in generated reports before relying on the output. <br>
Risk: Stock symbols and market interests may be sent to third-party quote or news services. <br>
Mitigation: Review network destinations before deployment and avoid submitting confidential portfolio or strategy information. <br>
Risk: Generated investment recommendations and indicators may be unreliable. <br>
Mitigation: Treat outputs as informational drafts and require human financial review before any trading or advisory use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/gaoren-stock-advanced) <br>
- [README.md](artifact/README.md) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [Futu HK stock page pattern](https://www.futunn.com/stock/{code}-HK) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text stock-analysis report with inline command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party market data, technical indicators, analyst ratings, and trading suggestions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
