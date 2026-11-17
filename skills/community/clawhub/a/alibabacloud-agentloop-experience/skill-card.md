## Description: <br>
Proactively retrieves prior Alibaba Cloud AgentLoop experience through the bundled SearchContext CLI when prior work, comparable incidents, historical fixes, or lessons learned may help an agent complete a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and coding agents use this skill to search prior Alibaba Cloud AgentLoop troubleshooting, remediation, and workflow experience before or during implementation and debugging tasks. The skill helps agents recall relevant historical context while requiring approval before transmitting query text to the configured endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recall queries may include task, error, incident, service, request, case, or file-path details and can be sent to a configured AgentLoop endpoint using local credentials. <br>
Mitigation: Use explicit per-query approval, redact secrets or regulated data before recall, and avoid using recall for confidential incident details unless the endpoint and data handling are approved. <br>
Risk: Broad trigger guidance can cause agents to perform outbound recall early in a task. <br>
Mitigation: Keep AGENTLOOP_CONFIRM_OUTBOUND unset unless operationally required, require --confirm-outbound for recall commands, and continue the task without blocking when recall is disabled or returns no results. <br>
Risk: Recalled content may be stale, irrelevant, or inconsistent with the current repository, logs, or user request. <br>
Mitigation: Treat recall results as context only and verify them against current evidence before acting. <br>


## Reference(s): <br>
- [SearchContext CLI](references/search-context-cli.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-agentloop-experience) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns a request_id, error value, and results array; recall requires explicit outbound confirmation unless AGENTLOOP_CONFIRM_OUTBOUND is enabled after approval.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
