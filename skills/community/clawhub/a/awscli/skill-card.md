## Description: <br>
Manage AWS Lightsail instances using AWS CLI for listing, starting, stopping, and rebooting allowed instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HypertextAssassinRajith](https://clawhub.ai/user/HypertextAssassinRajith) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to let an agent list and manage approved AWS Lightsail instances through configured AWS credentials and a constrained instance allowlist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start, stop, or reboot AWS Lightsail instances using configured AWS credentials. <br>
Mitigation: Use a dedicated least-privilege IAM user or role, keep ALLOWED_INSTANCES narrow, and require explicit human approval before start, stop, or reboot actions, especially for production resources. <br>
Risk: An overly broad ALLOWED_INSTANCES configuration can allow unintended instance operations. <br>
Mitigation: Set ALLOWED_INSTANCES to exact approved instance names and review allowlist changes before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Status messages] <br>
**Output Format:** [JSON objects returned to the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [List actions return AWS Lightsail instance data; start, stop, and reboot actions return success status messages.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
