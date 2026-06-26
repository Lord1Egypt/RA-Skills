## Description: <br>
Generates China Sports Lottery DLT number suggestions using historical-draw analysis, weighted number pools, strategy fusion, constraints, and backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensr](https://clawhub.ai/user/lovensr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can generate recreational DLT lottery number combinations, compound bet sets, and backtest summaries from historical draw data. Outputs should be treated as entertainment and analysis, not as financial advice or a reliable way to improve lottery odds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery recommendations can be mistaken for financial advice or a way to improve odds despite random lottery outcomes. <br>
Mitigation: Present outputs as entertainment only, avoid return or guarantee language, and encourage strict spending limits. <br>
Risk: Users may violate local gambling rules or spend more than intended when acting on generated bet combinations. <br>
Mitigation: Tell users to follow local gambling laws and set clear budget limits before using any generated combinations. <br>
Risk: The skill relies on configured local spreadsheet paths for historical data, so missing or stale data can make outputs misleading or fail at runtime. <br>
Mitigation: Verify the spreadsheet path and data freshness before prediction or backtesting. <br>
Risk: Artifact behavior includes joblib or pickle model persistence, which is unsafe with untrusted model files. <br>
Mitigation: Load only model files created by a trusted run of this skill and never load untrusted joblib or pickle files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lovensr/dlt-lottery-prediction) <br>
- [Publisher profile](https://clawhub.ai/user/lovensr) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Strategy fusion design](artifact/STRATEGY_FUSION_DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown-style explanatory text and Python dictionary outputs containing single-bet numbers, compound-bet numbers, validation results, scores, and backtest summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the configured DLT spreadsheet path and may include confidence-like scores or strategy labels that should not be interpreted as guaranteed outcomes.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
