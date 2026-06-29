## Description: <br>
Multi-factor weighted decision matrix with sensitivity analysis for hard choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to compare several options with weighted criteria, sensitivity analysis, and a concise recommendation report for complex decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recommendation can be misleading if the user provides biased weights, incomplete criteria, or subjective scores. <br>
Mitigation: Review the weights and scores, include explicit caveats, and use the sensitivity analysis to show whether the top-ranked option is stable. <br>
Risk: Users may include sensitive personal or business decision data while comparing options. <br>
Mitigation: Ask only for the information needed to score the options and remind users to share sensitive details only when they are comfortable doing so. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/decision-matrix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision report with weighted-score tables, sensitivity analysis, recommendations, and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided options, criteria, weights, and scores; does not request sensitive access or make system changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
