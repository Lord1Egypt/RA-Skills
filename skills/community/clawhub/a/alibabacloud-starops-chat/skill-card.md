## Description: <br>
Alibaba Cloud STAROps Agent AIOps diagnostic skill for diagnosing service errors, root causes, workspace topology, service metrics, APM signals, and incidents through STAROps Agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to ask STAROps diagnostic questions, create or continue investigation threads, and receive structured answers for incident triage. The skill is for diagnosis and evidence gathering, not direct cloud resource management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent query STAROps using the caller's Alibaba Cloud credential chain. <br>
Mitigation: Use least-privilege RAM permissions limited to starops:CreateThread and starops:CreateChat, and confirm the configured endpoint, workspace, employee ID, and UID before running. <br>
Risk: STAROps diagnostic output may contain sensitive operational data. <br>
Mitigation: Treat returned findings, metrics, topology, traces, and incident details as sensitive and share or store them only according to the user's operational security policy. <br>
Risk: Diagnostic conclusions can be misleading if they are not grounded in the returned STAROps answer. <br>
Mitigation: Base final reports only on content between the STAROPS ANSWER delimiters, retry once on empty or generic results with the same thread, and report honestly when STAROps returns no actionable data. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/sdk-team/alibabacloud-starops-chat) <br>
- [STAROps Agent API Reference](references/api-reference.md) <br>
- [STAROps RAM Policy Notes](references/ram-policies.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Structured pipe output with THREAD, STAROPS_URL, and delimited diagnostic answer text; JSONL is available only when explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STAROps configuration, Alibaba Cloud credential-chain credentials, and the --pipe flag for agent invocations.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
