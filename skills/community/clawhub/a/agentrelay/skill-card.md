## Description:

Reliable agent-to-agent communication protocol for transferring large payloads via shared files with pointer references and secret code verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use AgentRelay to pass large inter-agent payloads by storing content in shared files and sending short AgentRelay CSV pointers with completion verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay inputs may access paths outside the intended storage area.

Mitigation: Use only trusted AgentRelay messages until event IDs and pointers are validated and storage-directory containment is enforced.

Risk: Verification secrets are stored in plaintext and may be logged or returned.

Mitigation: Use non-sensitive payloads, avoid sharing relay secrets in logs, and replace the six-character secret with a cryptographic token before handling sensitive workflows.

Risk: Automatic handling from untrusted message text can trigger unintended file operations.

Mitigation: Review the sender and message before execution, and avoid enabling automatic handling for untrusted AgentRelay prefixes.

## Reference(s):

- [AgentRelay ClawHub skill page](https://clawhub.ai/extraterrest/skills/agentrelay)
- [AgentRelay documentation](https://docs.openclaw.ai/skills/agentrelay)
- [ClawHub publisher profile](https://clawhub.ai/user/extraterrest)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples; runtime commands emit JSON and CSV text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates shared relay files, registry records, and transaction logs under the configured OpenClaw data directory.]

## Skill Version(s):

1.1.1 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
