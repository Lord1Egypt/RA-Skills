## Description: <br>
CordysCRM helps an agent translate natural-language CRM requests into Cordys CRM CLI commands for intent recognition, module selection, parameter completion, pagination, L2C tracing, funnel analysis, and role-aware summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fit2-zhao](https://clawhub.ai/user/fit2-zhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and CRM operators use this skill to query Cordys CRM, inspect lead-to-cash workflows, review sales and finance status, and prepare command-line CRM actions with concise business summaries. It is suited for role-aware sales, manager, executive, contract administration, and finance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive powerful authenticated CRM and admin actions, including approvals, batch approval operations, raw API calls, and approval-flow changes. <br>
Mitigation: Install only from a trusted publisher, use least-privilege Cordys CRM credentials, and require explicit human confirmation before approvals, batch operations, raw API calls, or approval-flow changes. <br>
Risk: Cordys CRM credentials are required and could be exposed if requests are sent to an untrusted CRM domain or broad admin keys are stored in the skill environment. <br>
Mitigation: Keep CORDYS_CRM_DOMAIN restricted to a trusted Cordys CRM host, avoid enabling CORDYS_ALLOW_UNTRUSTED, and do not store broad admin keys in the skill .env file. <br>


## Reference(s): <br>
- [Cordys CRM API reference](references/crm-api.md) <br>
- [Cordys CRM CLI semantic specification](core/cli-spec.md) <br>
- [CordysCRM ClawHub skill page](https://clawhub.ai/fit2-zhao/cordys-crm) <br>
- [fit2-zhao publisher profile](https://clawhub.ai/user/fit2-zhao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise tabular summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference environment variables for Cordys CRM credentials and domain configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
