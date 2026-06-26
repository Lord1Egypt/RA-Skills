## Description: <br>
Assists agents with production incident response, including severity assessment, log analysis, debugging, root cause analysis, mitigation planning, recovery validation, and post-mortem documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to triage production incidents, analyze logs, metrics, and traces, and prepare mitigation, recovery, and post-mortem guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose high-impact production operations such as remediation, rollback, debugger attachment, packet capture, pod exec, cache changes, or log cleanup. <br>
Mitigation: Use least-privilege credentials, verify the target host or cluster, and require explicit human approval before running any production-changing command. <br>
Risk: Incident guidance can be incomplete or mismatched to the live environment during an outage. <br>
Mitigation: Validate recommendations against current telemetry and local runbooks, apply changes incrementally, monitor the four golden signals, and document actions for review. <br>


## Reference(s): <br>
- [Incident Responder code examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline command, code, SQL, YAML, and incident-report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose diagnostic and remediation commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
