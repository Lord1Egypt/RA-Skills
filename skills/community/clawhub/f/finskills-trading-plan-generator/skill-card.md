## Description:

Generate structured trade plans with entry, stop-loss, and take-profit levels based on technical and fundamental data from the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and analysts use this skill to turn a stock or ETF idea into a structured trading plan with entry triggers, stop-loss levels, profit targets, position sizing, and monitoring checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the Finskills service and requires storing a FINSKILLS_API_KEY.

Mitigation: Install only if use of the Finskills service is acceptable, store the API key securely, and avoid sharing it in prompts or generated output.

Risk: Trading-plan inputs can include sensitive personal financial details such as account size and risk tolerance.

Mitigation: Share approximate account size or risk limits where possible and avoid unnecessary personal financial details.

Risk: Generated trade plans may be incorrect, incomplete, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as educational analysis, verify market data and assumptions independently, and use personal judgment before trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/finskills-trading-plan-generator)
- [Project homepage](https://github.com/finskills/trading-plan-generator)
- [Finskills API service](https://finskills.net)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown trading plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and user-provided trade context such as symbol, thesis, direction, account size or approximate risk limits, and time horizon.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
