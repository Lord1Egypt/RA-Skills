## Description:

DataGuard DLP is designed to provide runtime data loss prevention for OpenClaw agents by scanning outbound tool calls for credential, PII, sensitive-data, domain, and recent sensitive-file context signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffcgit](https://clawhub.ai/user/jeffcgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add advisory runtime scanning, approvals, and local audit logging around OpenClaw outbound tool calls. It is intended for workflows that need help reducing accidental credential, PII, and sensitive-data transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill as a strong DLP boundary even though the security review says protection does not reliably match its claims.

Mitigation: Treat it as advisory scanning and local logging unless hook parsing, unknown-domain approval, context scoring, and configuration enforcement have been reviewed and fixed.

Risk: Automatic enforcement depends on OpenClaw hook support; without hooks, outbound operations are not intercepted automatically.

Mitigation: Deploy only where the pre-hooks are installed and tested; otherwise require agents to run the scanner manually before outbound operations.

Risk: Context tracking depends on explicit logging after sensitive reads.

Mitigation: Require workflows that read sensitive files to log those reads and review audit logs for missing context before relying on risk scoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffcgit/skills/dataguard-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw hook support for automatic pre-hook enforcement; otherwise the skill degrades to manual scanning.]

## Skill Version(s):

2.2.0 (source: frontmatter, release metadata, VERSION.text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
