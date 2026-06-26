## Description: <br>
Create and manage automation workflows for repetitive tasks such as scheduled data syncs, chained API calls, triggered actions, if-this-then-that automation, and multi-step business workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to define YAML-based workflows that run scheduled or triggered actions such as HTTP requests, Telegram notifications, transformations, and data sync jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daemon scheduling is unsafe for production automation. <br>
Mitigation: Avoid daemon mode until scheduling is fixed; test workflows with one-time runs before deployment. <br>
Risk: Network and secret-handling behavior is under-scoped for real workflows. <br>
Mitigation: Use only trusted workflow YAML, provide a minimal environment file with only required secrets, restore normal HTTPS verification, and add destination allowlists, rate limits, and approval checks before connecting to messaging, webhooks, or business APIs. <br>


## Reference(s): <br>
- [Automation Workflow Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/flow-automation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow YAML, command invocations, and operational setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
