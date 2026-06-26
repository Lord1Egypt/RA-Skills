## Description: <br>
Deerflow submits and monitors multi-step deep research tasks against a running DeerFlow LangGraph API-only deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Deerflow to submit asynchronous deep research requests to a trusted DeerFlow service and retrieve run identifiers or completed reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts are sent to the configured DeerFlow endpoint and may be processed by that service's model or search providers. <br>
Mitigation: Use the skill only with a DeerFlow endpoint you control or trust, and avoid sensitive prompts unless the endpoint and providers are approved for that data. <br>
Risk: The DeerFlow host is a separate deployment whose Docker images and configuration are outside this skill. <br>
Mitigation: Review the upstream DeerFlow deployment, images, credentials, and network exposure before operating the service. <br>


## Reference(s): <br>
- [Deerflow ClawHub release](https://clawhub.ai/bevanding/deerflow) <br>
- [DeerFlow upstream repository](https://github.com/bytedance/deer-flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON status objects and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits tasks to a configured DeerFlow LangGraph endpoint and prints thread_id, run_id, status, endpoint, or fetched run data.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
