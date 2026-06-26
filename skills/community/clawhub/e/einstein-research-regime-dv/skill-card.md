## Description: <br>
Detects structural macro regime transitions over a 1-2 year horizon using cross-asset ratio analysis across market concentration, yield curve, credit, size factor, equity-bond, and sector rotation signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run mechanical cross-asset regime analysis, classify the current macro regime, and produce strategic positioning guidance for long-horizon market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Financial Modeling Prep and requires an FMP API key for public market data. <br>
Mitigation: Provide the API key only in an environment where Financial Modeling Prep access is acceptable, and review API usage before execution. <br>
Risk: The generated regime assessment and portfolio posture guidance may be mistaken for personalized investment advice. <br>
Mitigation: Use the output as informational market analysis and require human review before applying it to investment decisions. <br>
Risk: The script writes timestamped JSON and Markdown reports to the configured output directory. <br>
Mitigation: Run it in a directory where generated market-analysis reports are expected and safe to retain. <br>


## Reference(s): <br>
- [Regime Detection Methodology](references/regime_detection_methodology.md) <br>
- [Indicator Interpretation Guide](references/indicator_interpretation_guide.md) <br>
- [Historical Regime Examples](references/historical_regimes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report, JSON report, and concise natural-language findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires market data access through Financial Modeling Prep using FMP_API_KEY; writes timestamped report files to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
