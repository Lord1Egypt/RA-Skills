## Description: <br>
Run a weighted decision matrix to score and rank 2-4 options across 5 configurable criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdomerofski](https://clawhub.ai/user/mdomerofski) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and external users use this skill to compare 2-4 options with weighted criteria and receive a ranked recommendation with plain-language reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision rankings depend on subjective user scores and weights, so the result can appear more objective than the inputs support. <br>
Mitigation: Show the selected criteria weights, explain that the winner reflects those inputs, and offer to rerun with adjusted weights for sensitivity testing. <br>
Risk: Option names or JSON inputs may include sensitive personal or business details. <br>
Mitigation: Avoid sensitive details unless appropriate for the agent environment, and use neutral labels when the exact details are not needed. <br>


## Reference(s): <br>
- [Decision Dynamo Criteria Reference](references/criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with ranked scores and optional shell-command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks 2-4 options across five weighted criteria; negative criteria are inverted before scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
