## Description: <br>
API Logger helps developers record, inspect, and analyze LLM API traffic through a local proxy with terminal and browser log viewers for prompts, responses, token usage, latency, and failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route LLM API calls through a local proxy, then review prompt and response history, token usage, latency, failures, and cost-related statistics during debugging or operational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool persistently captures full LLM conversations, including prompts, generated content, and token usage. <br>
Mitigation: Install only when full-fidelity API logging is intended; protect the log directory, limit routed traffic to approved use cases, and periodically delete retained logs. <br>
Risk: Logged content can be exported externally through the optional Feishu workflow. <br>
Mitigation: Use external export only after confirming the destination and reviewing the helper used for Feishu writes. <br>
Risk: The installer can configure a background proxy that continues running after setup. <br>
Mitigation: Verify the upstream API URL before routing traffic and disable background persistence when the proxy is not actively needed for debugging. <br>


## Reference(s): <br>
- [ClawHub API Logger release page](https://clawhub.ai/xiaohuaishu/api-logger) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for installing, configuring, running, and inspecting local API logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
