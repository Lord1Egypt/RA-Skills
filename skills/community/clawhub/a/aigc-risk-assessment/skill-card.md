## Description: <br>
Provides portfolio risk metrics, stress testing, and position management guidance using VaR, volatility, and position sizing calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBABYZS](https://clawhub.ai/user/GBABYZS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investment-analysis agents use this skill to calculate portfolio risk metrics and generate position management guidance for financial instruments. It supports VaR calculation, stress-testing workflows, and maximum position sizing based on capital, risk tolerance, price, and stop-loss inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk metrics and position sizing outputs can be mistaken for complete investment advice. <br>
Mitigation: Review calculations, assumptions, input data, and suitability before using outputs for financial decisions. <br>
Risk: The Python module depends on external market data and local scientific Python packages. <br>
Mitigation: Install dependencies deliberately and verify data freshness, coverage, and source reliability before relying on generated metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBABYZS/aigc-risk-assessment) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and JSON-like calculation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include numeric risk metrics, timestamps, error strings, and position sizing recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
