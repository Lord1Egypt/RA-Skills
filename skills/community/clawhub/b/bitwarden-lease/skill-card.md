## Description:

Bitwarden Lease helps agents install, operate, diagnose, and safely consume an owner-only macOS Bitwarden CLI lease with one native unlock for a 24-hour process-continuity window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and local agent operators use this skill to reduce repeated Bitwarden CLI unlock prompts while keeping the Bitwarden session inside a local owner-only broker. It supports installing or repairing the broker, checking lease status without prompting, unlocking only for authorized credentialed work, and consuming allowlisted Bitwarden operations without exposing session material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-level background broker holds a Bitwarden session in memory for up to 24 hours.

Mitigation: Install only from a pinned, reviewed revision and unlock only for authorized credentialed work.

Risk: Secret-bearing Bitwarden output can be captured by chat transcripts, logs, shell history, or files if handled casually.

Mitigation: Route secret output directly to the intended one-shot consumer and keep it out of transcripts, diagnostics, persistent files, and CI outputs.

Risk: Same-user local processes can request allowlisted Bitwarden operations while the lease is active.

Mitigation: Keep the runtime directory and socket owner-only, verify socket permissions no broader than 0600, and discard the lease when it is no longer needed.

## Reference(s):

- [Security contract](references/security-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret-bearing command output must be routed directly to the intended consumer and kept out of transcripts, logs, shell history, and files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
