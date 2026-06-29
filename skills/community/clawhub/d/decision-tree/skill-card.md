## Description: <br>
Guides agents through decision tree analysis for multi-stage decisions with uncertain outcomes, quantified probabilities, payoffs, rollback, sensitivity analysis, and EVPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to structure sequential choices with uncertainty, estimate branch probabilities and payoffs, roll expected values back through the tree, and identify sensitivity thresholds before recommending an option. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision tree outputs can influence business, financial, legal, or safety-relevant decisions. <br>
Mitigation: Treat the skill as a structured analysis aid; independently verify probabilities, payoffs, assumptions, and professional implications before acting. <br>
Risk: Incorrect or unjustified probabilities and mixed payoff units can produce misleading expected value recommendations. <br>
Mitigation: Require documented probability bases, consistent payoff units, sensitivity analysis, EVPI checks, and a missing-branch audit before relying on the recommendation. <br>


## Reference(s): <br>
- [Primary sources for decision-tree](references/sources.md) <br>
- [Magee 1964 chemical plant investment example](examples/magee-1964-chemical-plant-investment-hbr.md) <br>
- [Decision Tree skill page](https://clawhub.ai/deciqai/skills/decision-tree) <br>
- [deciqAI publisher profile](https://clawhub.ai/user/deciqai) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured decision tree tables and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes branch probabilities, payoff units, rollback calculations, sensitivity threshold, EVPI, and conditions where the recommendation changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
