## Description: <br>
Helps users structure decisions with SWOT, 10-10-10, decision trees, weighted scoring, and the Eisenhower matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose an appropriate decision framework, gather the needed inputs, and produce structured decision analysis without making the final choice for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad analysis or selection requests, which can be surprising or too heavy for simple questions. <br>
Mitigation: Narrow trigger wording or have the agent confirm before applying a decision framework when intent is ambiguous. <br>
Risk: Decision analyses can be misleading when user-provided weights, scores, probabilities, or assumptions are incomplete or biased. <br>
Mitigation: Ask for missing assumptions, label uncertainty, and use sensitivity checks or human review before acting on high-impact decisions. <br>


## Reference(s): <br>
- [Decision Tree Guide](references/decision-tree-guide.md) <br>
- [Frameworks Comparison](references/frameworks-comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown with tables, lists, tree diagrams, and optional weighted-scoring command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include key insights, recommendation tendencies, and uncertainty notes; final decisions remain with the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
