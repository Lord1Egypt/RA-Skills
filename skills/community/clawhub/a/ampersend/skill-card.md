## Description:

Ampersend CLI for agent payments

This skill is ready for commercial/non-commercial use.

## Publisher:

[matiasedgeandnode](https://clawhub.ai/user/matiasedgeandnode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up Ampersend CLI access, configure spending limits, and make x402 payment-enabled HTTP requests with JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable real autonomous payments through the Ampersend CLI.

Mitigation: Use it only for payment tasks the user explicitly intends, run inspect mode before paid fetches, and set tight daily, monthly, and per-transaction limits.

Risk: Payment keys or account details could be exposed through shell commands or agent-visible chat.

Mitigation: Avoid pasting real payment keys into shell commands or chats the agent can read; prefer user-controlled setup and review any configuration before activation.

Risk: The external CLI package receives payment authority after installation and configuration.

Mitigation: Verify npm package provenance before granting funds or credentials, and run the CLI in a constrained environment where practical.

Risk: Automatic top-up can increase financial exposure if enabled unnecessarily.

Mitigation: Avoid auto-topup unless required for the task and pair it with explicit spending limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matiasedgeandnode/skills/ampersend)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON and should be checked for ok status before using returned data.]

## Skill Version(s):

1.0.14 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
