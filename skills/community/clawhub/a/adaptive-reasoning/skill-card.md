## Description: <br>
Automatically assess task complexity and adjust reasoning level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzoricciulli](https://clawhub.ai/user/enzoricciulli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill as a pre-response check that scores request complexity and adjusts reasoning effort for complex questions, debugging, design, math, and high-stakes tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic reasoning escalation can increase latency and token usage for complex requests. <br>
Mitigation: Use this skill only where adaptive effort is desired, and disable or override it in workflows that require explicit reasoning control, strict latency, or strict token budgets. <br>
Risk: Reasoning indicators may change the visible response style. <br>
Mitigation: Review response-format requirements before deployment and remove or adapt the indicators if the deployment channel requires neutral formatting. <br>


## Reference(s): <br>
- [Adaptive Reasoning on ClawHub](https://clawhub.ai/enzoricciulli/adaptive-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with scoring tables, examples, and optional response indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no files, credentials, network access, code execution, or persistence requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
