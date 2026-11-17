## Description:

Logs tool calls before and after execution with parameters, results, errors, and session information for auditing and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add audit logging around agent tool calls for security review, debugging, usage analysis, and error tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs may capture sensitive tool inputs, outputs, user IDs, or session IDs.

Mitigation: Log minimal metadata by default, redact sensitive values before any log output, and apply strict access, retention, and deletion controls.

Risk: Example redaction may be ineffective for nested or unexpected sensitive fields.

Mitigation: Replace the sample redaction with tested recursive redaction before enabling the hook in environments that may process secrets, regulated data, or private file contents.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hook implementation examples, audit log format examples, and command-line analysis snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
