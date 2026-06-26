## Description: <br>
Query and interact with company knowledge bases or workflows through the Dify API with multi-turn context and streaming response support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whswhs1128](https://clawhub.ai/user/whswhs1128) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query Dify-backed knowledge bases, continue chat conversations, or run configured Dify workflows from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships a live-looking internal Dify base URL and bearer API key in documentation and code. <br>
Mitigation: Revoke or remove the bundled key before use, and provide DIFY_BASE_URL and DIFY_API_KEY through a secure environment configuration. <br>
Risk: Queries and conversation context are sent to the configured Dify service and may contain sensitive or regulated data. <br>
Mitigation: Use only approved Dify services and avoid sending secrets or regulated data unless the service and retention policy are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whswhs1128/dify-flow-access) <br>
- [Publisher profile](https://clawhub.ai/user/whswhs1128) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and Dify response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit streamed Dify responses, conversation IDs, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
