## Description: <br>
Analyzes China's macro climate across growth, inflation, exchange-rate, interest-rate, and credit dimensions to classify the macro cycle and produce broad asset-allocation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenge791](https://clawhub.ai/user/stevenge791) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts and developers use this skill to gather China macro indicators, compute percentile-based dimension scores, classify the economy with the Merrill Lynch investment clock, and draft a macro report with broad asset-allocation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Asset-allocation percentages and sector suggestions may be mistaken for personalized investment advice. <br>
Mitigation: Treat outputs as informational macro analysis, not personalized financial advice, and review conclusions with qualified judgment before use. <br>
Risk: Macro conclusions can be misleading if source data is stale, incomplete, or substituted with approximate indicators. <br>
Mitigation: Verify the underlying data, preserve confidence labels, and clearly mark missing or approximate indicators in the final report. <br>
Risk: Market-cycle classification near threshold values can overstate certainty. <br>
Mitigation: Use the skill's transition-zone warnings and compare recent score trends before acting on a single quadrant classification. <br>


## Reference(s): <br>
- [Indicator system](references/indicators.md) <br>
- [Scoring methodology](references/scoring-methodology.md) <br>
- [Merrill Lynch investment clock](references/merrill-lynch-clock.md) <br>
- [ClawHub release page](https://clawhub.ai/stevenge791/china-macro-climate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional JSON or text output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs macro-climate scores, cycle classification, confidence notes, and informational asset-allocation suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
