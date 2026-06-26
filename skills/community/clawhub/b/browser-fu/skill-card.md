## Description: <br>
Fixes browser automation failures with a snapshot-first workflow and API discovery behind website UIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whooshinglander](https://clawhub.ai/user/whooshinglander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to troubleshoot flaky browser interactions, inspect page state before acting, and prefer direct API discovery when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in browser profiles or cookie-backed requests can expose session tokens, cookies, or authenticated data beyond the requested task. <br>
Mitigation: Require explicit approval before using logged-in profiles or cookies, keep access scoped to the requested task, and do not store or output passwords, session tokens, or cookies. <br>
Risk: Direct API discovery can query internal or authenticated endpoints without the context and safeguards of the website UI. <br>
Mitigation: Check whether endpoints require authentication, get explicit approval before querying internal or authenticated APIs, respect automation blocks, and stop when access boundaries are unclear. <br>


## Reference(s): <br>
- [API Discovery Procedure](references/api-discovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown guidance with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend snapshot settings, browser actions, API calls, or curl commands depending on the task.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
