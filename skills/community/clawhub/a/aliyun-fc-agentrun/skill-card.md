## Description: <br>
Use when managing Function Compute AgentRun resources via OpenAPI (runtime, sandbox, model, memory, credentials), including creating runtimes/endpoints, querying status, and troubleshooting AgentRun workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud Function Compute AgentRun resources, including runtimes, runtime endpoints, sandboxes, model services, memory collections, credentials, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and delete real Alibaba Cloud AgentRun resources. <br>
Mitigation: Use least-privileged RAM or temporary STS credentials, confirm the target region and resource IDs before cleanup, and run only when resource changes are intended. <br>
Risk: Generated JSON response files may contain cloud resource metadata. <br>
Mitigation: Store generated response files privately and avoid sharing output directories without review. <br>


## Reference(s): <br>
- [AgentRun OpenAPI Overview](references/api_overview.md) <br>
- [AgentRun OpenAPI Service Endpoints](references/endpoints.md) <br>
- [AgentRun SDK Guidance](references/sdk.md) <br>
- [Source List](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under output/compute-fc-agentrun/ when scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
