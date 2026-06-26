## Description: <br>
Diagnose and manage Alibaba Cloud databases through natural language for performance troubleshooting, status checks, SQL optimization, health inspections, and security baseline review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DBAs, and cloud operations teams use this skill to ask DAS Agent natural-language questions about Alibaba Cloud database performance, connectivity, SQL tuning, instance health, and security baselines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad, credentialed access to Alibaba Cloud database management workflows. <br>
Mitigation: Use a dedicated least-privilege RAM role limited to the required DAS Chat permission and avoid production administrator or FullAccess credentials. <br>
Risk: Agent-driven database actions or recommendations could affect availability, data, billing, or account state. <br>
Mitigation: Require explicit human approval before taking any action that could change service state or incur cost. <br>
Risk: Prompts and multi-turn sessions may expose sensitive operational details or credentials. <br>
Mitigation: Do not put secrets in prompts, start a fresh session for unrelated work, and limit shared context to what the diagnostic task requires. <br>
Risk: The service has paid usage paths after trial or free-tier use. <br>
Mitigation: Confirm the intended DAS Agent subscription or quota before production use and monitor billing impact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-das-agent) <br>
- [DAS Agent API Reference](references/api-reference.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Alibaba Cloud credential configuration](https://www.alibabacloud.com/help/en/sdk/developer-reference/v2-manage-python-access-credentials) <br>
- [Alibaba Cloud API signature documentation](https://help.aliyun.com/document_detail/185337.htm) <br>
- [Alibaba Cloud RAM permission guide](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-a-ram-user) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Plain text or JSONL from the DAS client, typically relayed in Markdown by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a server-assigned session ID, progress events, tool-call events, and delimited diagnostic output depending on mode.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
