## Description: <br>
Prepares signed AICADE gateway service-management requests for service registration, service detail queries, and service disable operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aicadegalaxy](https://clawhub.ai/user/aicadegalaxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and service operators use this skill to gather AICADE service metadata, validate registration inputs, and generate signed curl commands for register/update, detail, and disable operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands may contain an API key, signature, timestamp, and nonce. <br>
Mitigation: Treat generated commands as sensitive and review them before running or sharing. <br>
Risk: Disable requests can change service availability if a user runs the generated command. <br>
Mitigation: Confirm the serviceId and disable operation with the user before generating the final signed curl. <br>
Risk: Registration flows may involve upstream service secrets. <br>
Mitigation: Prefer placeholders for upstream credentials unless the user intentionally provides real values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aicadegalaxy/aicade-create-service) <br>
- [Service Management API Reference](references/service-management-api.md) <br>
- [Register Service Guided Intake](references/register-intake.md) <br>
- [Service Operations Guided Intake](references/service-operations-intake.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and signed curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated curl commands may include API keys and signatures; the skill prints requests and does not call the remote API by itself.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
