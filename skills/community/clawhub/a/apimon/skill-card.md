## Description:

Apimon records API-related activity notes in local logs and supports searching, statistics, and JSON, CSV, or text export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps practitioners use Apimon to record API health, validation, linting, formatting, and report notes for later review or export. Treat it as a local activity log, not an automated uptime monitor, schema validator, or incident remediation tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake Apimon for an automated API monitor, uptime checker, or schema validator.

Mitigation: Use it only to record and review API-related notes unless independent monitoring or validation tools provide the underlying results.

Risk: Commands persist user-provided API details, URLs, incident notes, and exported records as plaintext local files.

Mitigation: Avoid entering tokens, headers, customer data, private URLs, or sensitive incident details unless local plaintext retention is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/apimon)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local text, JSON, or CSV export outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands write timestamped plaintext entries under ~/.local/share/apimon and can export accumulated records.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
