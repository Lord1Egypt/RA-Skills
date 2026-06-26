## Description: <br>
Routes agent tool requests through Clawvisor for credential vaulting, task-scoped authorization, policy enforcement, and human approval flows across connected services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlevine](https://clawhub.ai/user/ericlevine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route Gmail, Calendar, Drive, Contacts, GitHub, and iMessage actions through Clawvisor so credentials stay vaulted and requests can be scoped, audited, restricted, or sent for human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broadly scoped Clawvisor agent token can access sensitive connected services. <br>
Mitigation: Use a dedicated, narrowly scoped token and rotate or revoke it immediately if compromised. <br>
Risk: Standing or overly broad tasks can authorize more actions than a workflow needs. <br>
Mitigation: Prefer short-lived task scopes where possible and review standing tasks before approving them. <br>
Risk: Write or destructive actions could affect email, calendar, file, message, or repository data. <br>
Mitigation: Use the provided safe policies so write operations require approval and destructive actions are blocked or explicitly reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlevine/clawvisor) <br>
- [Clawvisor homepage](https://github.com/clawvisor/clawvisor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWVISOR_URL, CLAWVISOR_AGENT_TOKEN, and OPENCLAW_HOOKS_URL environment configuration.] <br>

## Skill Version(s): <br>
0.9.10 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
