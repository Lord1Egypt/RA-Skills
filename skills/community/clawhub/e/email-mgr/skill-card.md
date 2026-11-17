## Description:

Read, search, compose, and manage email. Inbox, search, compose, threading, status. JSON-based email store. Zero external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Email Manager to inspect, search, draft, and manage local JSON-backed email records from an agent or terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content and metadata may be stored in plaintext JSON.

Mitigation: Use only non-sensitive local email data unless filesystem permissions, storage location, and data retention are acceptable.

Risk: SMTP passwords or tokens placed in settings.json would be stored in plaintext.

Mitigation: Do not place SMTP passwords or tokens in settings.json; use an external secret store or a safer integration before handling real credentials.

Risk: The security evidence says documentation and implementation disagree for sensitive email and credential handling.

Mitigation: Review the implementation before installing and do not rely on documented send, dry-run, read, delete, interactive compose, or programmatic API behavior until corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/email-mgr)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output, Markdown guidance, shell command examples, and JSON-backed email records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON files for email records and settings; no external dependencies are declared.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact/clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
