## Description: <br>
Deploys the SupplyWhy application to a development EC2 and Kubernetes environment from Slack natural language commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yusong-7456](https://clawhub.ai/user/yusong-7456) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to trigger SupplyWhy development deployments from Slack natural language and receive deployment status. It is intended for workflows where the operator controls the Slack trigger and deployment authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack text can trigger real infrastructure changes with weak scoping and no built-in confirmation. <br>
Mitigation: Require explicit human confirmation, authenticated Slack triggers, and strict allowlists for permitted environments, tags, and deployment targets. <br>
Risk: The skill uses shell command construction around deployment inputs and remote commands. <br>
Mitigation: Validate and constrain all parsed values before execution, avoid unsafe shell interpolation, and log the exact approved deployment target before running commands. <br>
Risk: The skill requires access to the SupplyWhy SSH key and Kubernetes deployment authority. <br>
Mitigation: Install only in controlled workflows, limit key and Kubernetes permissions to the intended development environment, and retain auditable deployment records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yusong-7456/deploydevnlu) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yusong-7456) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Text status messages with shell command execution and remote deployment configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update an image tag or deployment target and reports deployment success or failure.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
