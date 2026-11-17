## Description:

Sign in to the wallet when a user wants to log in, connect, set up the wallet, or recover from wallet operations that fail with authentication or "not signed in" errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to authenticate a payments wallet through an email OTP flow when wallet operations require sign-in. It guides status checks, login initiation, OTP verification, and retrieval of wallet balance or address through the wallet CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to execute a mutable npm package with npx awal@latest during wallet authentication.

Mitigation: Run the skill only in a tightly sandboxed agent environment and prefer a version-pinned, reviewed wallet CLI before use.

Risk: The authentication flow may involve OTP codes and direct inbox access without clear consent boundaries.

Mitigation: Avoid granting mailbox access to the agent; have the user provide OTP codes manually with explicit consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrag/skills/authenticate-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can request machine-readable JSON output with --json.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
