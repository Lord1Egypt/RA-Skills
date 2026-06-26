## Description: <br>
AgentPathfinder creates cryptographically signed audit trails for AI agent tool calls, logs full arguments and results, and surfaces failures, hanging calls, false success claims, and HMAC verification in a local dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to instrument AI agent work with signed tool-call records, inspect local audit trails and dashboards, and identify failed, hanging, or falsely reported execution steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local command, file, network, dashboard, and plaintext logging capabilities can expose sensitive command arguments or results. <br>
Mitigation: Use the skill in an isolated workspace, avoid logging secrets, protect ~/.agentpathfinder, and review audit output before sharing. <br>
Risk: HMAC signatures and dashboards are audit aids, not independent proof that requested work was actually completed. <br>
Mitigation: Verify completion with external checks such as tests, CI status, artifact hashes, service health checks, or human review. <br>
Risk: Local audit data may be accessible to processes with filesystem access to the audit directory. <br>
Mitigation: Restrict filesystem permissions, use separate users or isolated environments, and keep audit storage outside untrusted agent write scope where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/certainlogicai/certainlogic-pathfinder) <br>
- [Safety and Security Disclosure](SAFETY.md) <br>
- [README](README.md) <br>
- [Honest Product Definition](HONEST_PRODUCT_DEFINITION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples; runtime artifacts include signed JSONL audit logs and HTML or JSON dashboard reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first audit records may include full command arguments, results, timestamps, and HMAC signatures.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
