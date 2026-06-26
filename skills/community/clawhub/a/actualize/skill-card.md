## Description: <br>
Reconcile the project's FPF state with recent repository changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hahamumu08](https://clawhub.ai/user/hahamumu08) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit recent repository changes against an FPF knowledge base, identify context drift, stale evidence, and decisions that may need review, then update the FPF baseline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository and .fpf files to assess freshness, which may surface project context or assurance-case details in the agent session. <br>
Mitigation: Run it only in repositories where the agent is allowed to inspect project and .fpf content. <br>
Risk: The skill can update .fpf/.baseline, which changes the recorded actualization point. <br>
Mitigation: Review the baseline update and any proposed context changes before committing them. <br>


## Reference(s): <br>
- [Actualize on ClawHub](https://clawhub.ai/hahamumu08/actualize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with git command guidance and baseline configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update .fpf/.baseline after reporting findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
