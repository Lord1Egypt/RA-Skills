## Description: <br>
Compliance Audit provides a local, tamper-evident audit trail for autonomous agent skill executions, data access, decisions, and budget changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trypto1019](https://clawhub.ai/user/Trypto1019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agent operators, and governance teams use this skill to record, inspect, verify, export, and summarize local audit logs for incident response, budget accountability, trust verification, enterprise compliance, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent audit logs can contain secrets, personal data, or regulated data if callers include them in entry details. <br>
Mitigation: Do not log API keys, tokens, passwords, PII, or regulated data; set appropriate file permissions and retention or deletion practices for ~/.openclaw/audit. <br>
Risk: Exported audit data can disclose sensitive operational history. <br>
Mitigation: Review JSON and CSV exports before sharing them outside the intended governance or incident-response audience. <br>
Risk: Unsafe shell construction around JSON arguments can corrupt entries or expose untrusted input handling issues. <br>
Mitigation: Pass JSON arguments safely from the invoking agent without shell string concatenation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Trypto1019/arc-compliance-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime script output includes plain text summaries, JSON exports, CSV exports, and daily JSON audit files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local daily audit logs under ~/.openclaw/audit/ when invoked; requires python3 on Linux or macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
