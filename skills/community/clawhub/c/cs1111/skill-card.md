## Description:

Collects system, network, and filesystem diagnostic information and can generate structured JSON or Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiqi704](https://clawhub.ai/user/qiqi704)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill for authorized local diagnostics, security checks, and environment reports across system, network, and filesystem areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute unrestricted shell commands as the agent user.

Mitigation: Use it only in trusted workspaces, avoid passing untrusted input to custom command execution, and review commands before running them.

Risk: Diagnostic reports may contain host, user, network, environment, and filesystem details.

Mitigation: Review and redact generated reports before sharing or storing them outside the authorized environment.

Risk: Network diagnostics contact external hosts and may disclose local network behavior.

Mitigation: Run network checks only where external connectivity tests are authorized and expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiqi704/skills/cs1111)
- [Publisher profile](https://clawhub.ai/user/qiqi704)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus JSON or Markdown diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include host, user, network, environment, and filesystem details.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
