## Description: <br>
Dynamically selects the best AI model for a task based on complexity, cost, and availability in GitHub Copilot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpelissari](https://clawhub.ai/user/mpelissari) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to classify a prompt or task and choose a GitHub Copilot model that balances task complexity, expected capability, and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model availability, pricing, and cost information may become outdated. <br>
Mitigation: Review the model reference and current GitHub Copilot availability before relying on recommendations for production workflows. <br>
Risk: Highly sensitive prompts passed as shell arguments may be retained in shell history. <br>
Mitigation: Avoid passing highly sensitive content directly on the command line; redact sensitive details or use a safer input path before classification. <br>
Risk: Heuristic classification can recommend a model that is not suitable for a specific high-impact task. <br>
Mitigation: Treat recommendations as guidance and verify the model choice before using it for high-impact work. <br>


## Reference(s): <br>
- [Available GitHub Copilot Models - Detailed Specs](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text recommendation with a model name, reason, and cost tier; Markdown guidance when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are heuristic and may become outdated as GitHub Copilot model availability changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
