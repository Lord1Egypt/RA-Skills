## Description: <br>
Manage Function Compute AgentRun resources via OpenAPI for runtimes, sandboxes, model services, memory, credentials, endpoint creation, status checks, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to operate Alibaba Cloud Function Compute AgentRun resources, including creating runtimes and endpoints, checking resource status, and troubleshooting AgentRun workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can delete AgentRun runtime endpoints and runtimes when run with real resource IDs. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials and verify region, runtime ID, and endpoint ID before running cleanup. <br>
Risk: Generated API response files may contain operational details from the target Alibaba Cloud account. <br>
Mitigation: Review generated response files before sharing or committing them. <br>


## Reference(s): <br>
- [AgentRun OpenAPI overview](references/api_overview.md) <br>
- [AgentRun OpenAPI endpoints](references/endpoints.md) <br>
- [AgentRun SDK guidance](references/sdk.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-compute-fc-agentrun) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated API response summaries are written under output/compute-fc-agentrun/responses when scripts are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
