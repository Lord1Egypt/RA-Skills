## Description: <br>
Agent Security DLP helps agents check inputs, memory, tool calls, and outputs for prompt-injection patterns and sensitive data using configurable DLP rules and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add DLP checks around agent inputs, memory, tool use, and responses, including detection, redaction or blocking, approval hints, and audit logs for sensitive-data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit logging may store checked content or sensitive memory data locally by default. <br>
Mitigation: Review config/config.json before installation; disable audit logging or redirect logs to a protected and redacted location before using real secrets, PII, or private memory data. <br>
Risk: Tool checks can mark dangerous tools as requiring approval, but integrations must enforce the approval decision. <br>
Mitigation: Treat require_approval as a policy decision that the calling agent or orchestrator must block or route to human approval before executing the tool. <br>
Risk: Documented protections are not a guarantee that every secret, PII type, or prompt-injection attempt will be caught. <br>
Mitigation: Use the skill as a defense-in-depth check, test it against organization-specific data patterns, and keep stricter policies for high-risk workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caidongyun/agent-security-dlp) <br>
- [README](artifact/README.md) <br>
- [Rule Exploration](artifact/docs/RULE_EXPLORATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON-like check results, and audit log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sanitized text, block decisions, findings, approval-required flags, and local audit log records.] <br>

## Skill Version(s): <br>
2.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
