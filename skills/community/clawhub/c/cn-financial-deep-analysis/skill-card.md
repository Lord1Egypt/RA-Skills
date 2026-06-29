## Description: <br>
CN Financial Deep Analysis helps agents produce A-share financial analysis and research reports using a macro, statement-level, and account-level framework with financial indicators, fraud warning signals, and industry benchmarking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to screen A-share companies for financial risk, produce deep company analysis, compare industries, and draft structured equity research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Python, MCP, chart, and Word-export components introduce dependency hygiene and installation risk. <br>
Mitigation: Install optional components only when needed, use a virtual environment, review the external cn-financial-mcp repository before installation, and prefer pinned or currently patched dependency versions. <br>
Risk: Generated financial analysis and investment recommendations may be incomplete, stale, or unsuitable for decision-making without review. <br>
Mitigation: Treat outputs as research assistance only and verify them against official filings or a qualified financial professional before using them for investment decisions. <br>


## Reference(s): <br>
- [CN Financial Deep Analysis on ClawHub](https://clawhub.ai/tuobadaidai/skills/cn-financial-deep-analysis) <br>
- [Three-Layer Financial Analysis Framework](artifact/references/core/three-layer-framework.md) <br>
- [Fraud Detection Framework](artifact/references/core/fraud-detection.md) <br>
- [Financial Scoring System](artifact/references/core/scoring-system.md) <br>
- [Fraud Case Library](artifact/references/cases/README.md) <br>
- [Industry Analysis References](artifact/references/industries/README.md) <br>
- [cn-financial-mcp Data Connector](https://github.com/ccq1/cn-financial-mcp.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional PNG charts and Word documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional Python tooling can generate charts and Word exports when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
