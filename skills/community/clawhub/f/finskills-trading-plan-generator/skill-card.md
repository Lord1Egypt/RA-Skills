## Description: <br>
Generate structured trade plans with entry, stop-loss, and take-profit levels based on technical and fundamental data from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to turn a stock or ETF idea into a structured trading plan with entries, stops, targets, position sizing, and thesis validation using Finskills market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Finskills API key and may involve portfolio or trade details. <br>
Mitigation: Use a dedicated API key, keep credentials out of shared prompts and logs, and avoid sharing unnecessary portfolio details. <br>
Risk: Generated trade plans can be incorrect, incomplete, or unsuitable for the user's circumstances. <br>
Mitigation: Independently verify market data, assumptions, position sizing, and risk controls before acting on any plan. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/finskills/finskills-trading-plan-generator) <br>
- [Project homepage](https://github.com/finskills/trading-plan-generator) <br>
- [Finskills API](https://finskills.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown trade plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and user-provided trade context such as symbol, direction, account size, risk tolerance, and time horizon.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
