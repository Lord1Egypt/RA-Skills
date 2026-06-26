## Description: <br>
Monitor early-warning signals of AI-driven white-collar labor displacement and macro-financial spillovers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, investors, and risk teams use this skill to build a structured monitor for AI-led labor substitution, employment stress, consumption and credit spillovers, and concise portfolio or risk-posture notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can produce misleading alerts if source data is stale, partial, or not independently verified. <br>
Mitigation: Timestamp every metric, list missing or stale inputs under data gaps, and verify current labor, credit, market, and portfolio data from trusted sources before acting. <br>
Risk: Threshold-based risk lights may be interpreted as authoritative financial advice or a complete macro model. <br>
Mitigation: Use outputs as decision-support only, review portfolio actions with appropriate domain experts, and define stricter numeric thresholds when repeatable decisions are required. <br>


## Reference(s): <br>
- [Thresholds example](references/thresholds.example.json) <br>
- [ClawHub skill page](https://clawhub.ai/spyfree/ai-displacement-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/spyfree) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown signal board with an optional JSON mode when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes latest-value signal status, composite risk light, actionable notes, confidence, and data gaps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
