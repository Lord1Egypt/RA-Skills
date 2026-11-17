## Description:

Breaker presents as a circuit breaker task tool and provides a local CLI for recording, listing, searching, exporting, and configuring entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to invoke a local shell-based record manager for breaker-related notes or task entries. It should not be relied on for electrical breaker sizing or coordination decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release presents itself as an electrical breaker sizing and coordination tool, but the inspected code behaves as a local record manager.

Mitigation: Do not rely on this skill for electrical breaker sizing, coordination, compliance, or safety-critical decisions; use it only for local notes after review.

Risk: The script persists entries, supports export and deletion, and includes an unsafe configuration update path.

Mitigation: Inspect the shell serialization and sed-based config update logic before installation, avoid untrusted configuration values, and do not store sensitive data in the tool.

## Reference(s):

- [Breaker ClawHub skill page](https://clawhub.ai/bytesagain1/skills/breaker)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; script output is plain text with optional JSONL or CSV export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local data under the configured BREAKER_DIR path, defaulting to ~/.breaker/.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
