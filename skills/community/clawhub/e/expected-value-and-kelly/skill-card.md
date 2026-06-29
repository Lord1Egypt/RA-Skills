## Description: <br>
Helps an agent evaluate repeated sizing decisions by mapping probabilities and payoffs, computing expected value, applying the Kelly criterion or fractional Kelly, and naming stop triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through repeated capital-allocation, position-sizing, ad-spend, A/B-test ramp, or similar decisions where probabilities and payoffs can be estimated. The skill produces an EV-Kelly sizing analysis with uncertainty, fractional-Kelly, correlation, and stop-trigger checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat educational EV-Kelly output as professional financial advice or apply it to one-shot decisions. <br>
Mitigation: Present outputs as educational analysis, require a repeatable decision with estimable probabilities and payoffs, and redirect one-shot or unestimable decisions away from Kelly sizing. <br>
Risk: Incorrect probabilities, payoffs, or correlation assumptions can lead to oversized recommendations. <br>
Mitigation: Require explicit input uncertainty, fractional-Kelly sizing, correlation checks, and concrete stop-and-reestimate triggers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/expected-value-and-kelly) <br>
- [Sources - expected-value-and-kelly](references/sources.md) <br>
- [A New Interpretation of Information Rate](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf) <br>
- [The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market](https://www.eecs.harvard.edu/cs286r/courses/fall12/papers/Thorpe_KellyCriterion2007.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown EV-Kelly sizing worksheet with calculations and decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational calculation guidance; no executable behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
