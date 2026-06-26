## Description: <br>
Logs tool calls before and after execution with parameters, results, errors, and session information for auditing and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add audit logging around agent tool calls so they can review tool usage, errors, sessions, and debugging context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly logs tool activity and may capture sensitive context or raw tool results. <br>
Mitigation: Log metadata by default, restrict audit log access, define retention and cleanup, and record raw parameters or results only when explicitly needed. <br>
Risk: The described sensitive-data handling may provide incomplete redaction for nested values or unexpected secret field names. <br>
Mitigation: Apply recursive redaction before writing any log entry and test redaction coverage for tokens, passwords, secrets, API keys, and organization-specific sensitive fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxiao-bot/audit-log-hook) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for hook registration, audit log entries, basic sensitive-field redaction, and command-line log analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
