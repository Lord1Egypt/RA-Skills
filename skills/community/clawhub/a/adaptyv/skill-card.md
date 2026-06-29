## Description: <br>
Guides agents in using the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzk1121](https://clawhub.ai/user/yzk1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to work with Adaptyv's authenticated Foundry API for protein screening, binding, thermostability, expression, and fluorescence experiment workflows. It helps draft API calls, Python SDK usage, token handling, cost-estimation, experiment submission, webhook, and result retrieval guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers authenticated API workflows that use sensitive Adaptyv credentials. <br>
Mitigation: Keep API keys scoped and out of source control; use environment variables or local .env files for credentials. <br>
Risk: Some documented experiment flows can submit billable lab work or create invoices. <br>
Mitigation: Review cost estimates and quote confirmations before submission; use auto_accept_quote only when a billable invoice is intended. <br>
Risk: Webhook configuration can send experiment status updates to external endpoints. <br>
Mitigation: Configure webhook URLs only for endpoints controlled by the user or organization. <br>


## Reference(s): <br>
- [Adaptyv Bio Foundry API endpoint reference](references/api-endpoints.md) <br>
- [Adaptyv Foundry API base URL](https://foundry-api-public.adaptyvbio.com/api/v1) <br>
- [Adaptyv Foundry portal](https://foundry.adaptyvbio.com/) <br>
- [ClawHub release page](https://clawhub.ai/yzk1121/adaptyv) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yzk1121) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, Python SDK snippets, environment variable names, and workflow checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
