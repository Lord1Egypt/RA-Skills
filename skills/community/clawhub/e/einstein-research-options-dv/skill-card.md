## Description:

Educational options analysis and simulation support using Black-Scholes pricing, Greeks, and risk-focused explanations for evaluating strategy setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to review options strategy tradeoffs, estimate theoretical option prices and Greeks, and understand risk exposure before execution. It is intended for educational analysis and does not execute trades or replace professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release materially overstates its implemented options strategy simulator capabilities.

Mitigation: Use it only as an educational Black-Scholes and Greeks helper unless the missing analyzer is added and validated.

Risk: Market-data access and credential handling are under-specified.

Mitigation: Install dependencies in an isolated environment and use a limited FMP API key with quota controls.

Risk: The outputs may be mistaken for actionable trading advice.

Mitigation: Present results as educational analysis, preserve not-financial-advice disclaimers, and require human review before any trade decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-options-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Natural-language Markdown with optional command examples, JSON-style analysis summaries, and calculated pricing or Greeks values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated analysis files, P/L summaries, risk warnings, and educational disclaimers when supported by the available script behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
