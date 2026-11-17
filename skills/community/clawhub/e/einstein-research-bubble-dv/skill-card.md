## Description:

Evaluates market bubble risk through quantitative, data-driven analysis using a revised Minsky/Kindleberger framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess market-level bubble risk from quantitative indicators, historical context, and limited evidence-based qualitative checks. It is intended to support risk review and portfolio posture discussions, not to provide personalized financial advice or exact market-timing predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete investment, hedging, profit-taking, and short-selling guidance.

Mitigation: Treat outputs as educational market-risk analysis only; require human review before any portfolio action and do not use the skill as personalized financial advice.

Risk: Market-risk scoring depends on current and accurate market data.

Mitigation: Independently verify all indicator values, sources, and collection dates before relying on the score.

Risk: Install and run commands may use unpinned Python dependencies.

Mitigation: Run the skill in an isolated virtual environment and pin dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-bubble-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)
- [Detailed Bubble Theory Framework](references/bubble_framework.md)
- [Historical Bubble Cases and Pattern Analysis](references/historical_cases.md)
- [Bubble Detector Implementation Guide](references/implementation_guide.md)
- [Bubble Detection Quick Reference](references/quick_reference.md)
- [Bubble Detection Quick Reference (English)](references/quick_reference_en.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Natural-language analysis with optional Markdown reports, JSON reports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on current market data and user-supplied or freshly collected indicator values.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
