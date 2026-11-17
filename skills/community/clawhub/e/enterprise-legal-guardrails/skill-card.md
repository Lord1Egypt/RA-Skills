## Description:

Legal/compliance guardrails for outbound OpenClaw actions (anti-spam, defamation, privacy, financial claims).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawyered0](https://clawhub.ai/user/lawyered0)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to preflight outbound posts, comments, messages, market commentary, workplace-sensitive text, and privacy-sensitive content before publication or command execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional command-running wrapper can execute outbound commands and has unsafe bypass options.

Mitigation: Prefer direct checker-only use in production, or require strict mode, narrow absolute-path allowlists, sanitized environments, and no allow-any-command bypass.

Risk: Command arguments, audit logs, and inherited environment variables can contain sensitive information.

Mitigation: Use sanitized environments with narrow keep rules, bound command and checker timeouts, and handle audit logs as sensitive operational records.

## Reference(s):

- [Guardrail Policy Map](references/guardrail-policy-map.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text verdicts or JSON results, with shell command examples and policy guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns PASS, WATCH, REVIEW, or BLOCK; the wrapper can remain validation-only unless explicit execution is enabled.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
