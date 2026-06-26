## Description: <br>
Discover and send tasks to A2A agents via the A2A API Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thearchitectit](https://clawhub.ai/user/thearchitectit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover available A2A agents or providers, delegate tasks through an A2A API Gateway, and retrieve task status or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically uses admin-level gateway authentication for ordinary discovery and task operations. <br>
Mitigation: Install only when you control and trust the configured A2A gateway, and prefer a future version that uses least-privilege task and discovery tokens. <br>
Risk: Task prompts and results may contain sensitive information that is sent through the gateway and downstream providers. <br>
Mitigation: Avoid sending sensitive prompts or results unless the gateway and downstream providers are approved for that data. <br>
Risk: Gateway URLs and API keys are required for use. <br>
Mitigation: Keep gateway configuration and API keys out of shared logs and source-controlled configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thearchitectit/a2a-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3 on Linux or Darwin; outputs can include gateway discovery results, task identifiers, task metadata, token usage, and LLM responses.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
