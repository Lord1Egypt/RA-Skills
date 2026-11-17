## Description:

Agent Security DLP helps agents detect prompt injection and sensitive data in inputs, memory, tool calls, and outputs using configurable rules and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to add DLP checks around agent prompts, generated responses, memory content, and tool execution requests. It is intended for workflows that need configurable detection of credentials, personal data, regulated records, prompt-injection patterns, and high-impact tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked secrets, personal data, or regulated records may be written to a local plaintext audit log by default.

Mitigation: Disable audit logging or redesign it to store only redacted data in protected storage before using the skill with sensitive or regulated content.

Risk: Dangerous tool checks can signal that approval is required without enforcing the approval decision in the runtime.

Mitigation: Enforce tool approval in the calling agent or execution environment, and treat approval-required responses as policy gates before running high-impact tools.

Risk: Input protection may be overstated if an integration uses a lightweight path that does not call the real input guard.

Mitigation: Use the core AgentDLP input guard for prompt-injection checks and test the exact integration path before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caidongyun/skills/agent-security-dlp)
- [README](artifact/README.md)
- [Rule exploration plan](artifact/docs/RULE_EXPLORATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, Python integration snippets, and structured check results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include block or sanitize decisions, matched rule details, audit log access, and configuration guidance.]

## Skill Version(s):

2.1.3 (source: server release metadata; artifact changelog lists 2.1.1 and pyproject.toml lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
