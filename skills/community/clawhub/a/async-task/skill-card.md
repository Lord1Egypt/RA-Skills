## Description:

Async Task helps agents start, track, and complete long-running tasks without losing user-facing results to HTTP timeouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderfga](https://clawhub.ai/user/enderfga)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to keep long-running command execution, code analysis, multi-step work, or slow API calls responsive while sending completion or failure updates back to the active session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content may include secrets, private code, customer data, or sensitive logs.

Mitigation: Review use before installation in sensitive environments and avoid sending confidential content through task updates.

Risk: Session auto-detection or direct push behavior may send updates to the wrong active session in multi-session contexts.

Mitigation: Set OPENCLAW_SESSION explicitly and avoid direct push commands when multiple sessions are active.

Risk: Custom push endpoints can receive session-linked content with weak recipient or transport controls.

Mitigation: Use only trusted HTTPS endpoints with scoped authentication tokens.

Risk: The local async-task history file can retain sensitive task descriptions and results.

Mitigation: Treat the local async-task state and history file as sensitive and clear it according to local retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderfga/skills/async-task)
- [Publisher profile](https://clawhub.ai/user/enderfga)
- [Project repository link declared in package metadata](https://github.com/Enderfga/openclaw-async-task)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CLI usage examples, and environment variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue session update text through OpenClaw or Clawdbot CLI, or through a configured custom HTTP endpoint.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
