## Description: <br>
Provides multi-market financial analysis for historical data retrieval, financial statement parsing, financial ratio calculation, fixed income analysis, portfolio performance evaluation, and stock fundamental screening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial analysts use this skill to generate guidance, code, and command snippets for financial analysis workflows, including ratio analysis, data acquisition, backtesting, portfolio analytics, and risk or performance review across supported markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill expands beyond ratio analysis into trading strategy generation, backtesting, execution semantics, code generation, and durable skill-file writing. <br>
Mitigation: Review generated strategies, backtests, code, commands, and file writes before execution; deny skill-file creation or updates unless that behavior is specifically intended. <br>
Risk: The security guidance warns against giving the skill broker credentials, account access, broad filesystem write access, or purchase-enabling permissions by default. <br>
Mitigation: Run the skill with least privilege, avoid broker or account credentials unless required, and require explicit confirmation before any trading, purchasing, or account-impacting action. <br>
Risk: Artifact behavior includes market data provider selection, crypto coverage, and backtesting or trading workflow generation. <br>
Mitigation: Validate data sources, assumptions, entity IDs, time ranges, and generated order semantics before relying on outputs for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/financial-ratios-toolkit) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Financial Ratio Calculation Component](references/components/financial_ratio_calculation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for target market, data provider, strategy type, time range, and target entity IDs before generating workflow-specific output.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata; artifact metadata version v6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
