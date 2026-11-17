## Description:

Ampersend CLI for agent payments

This skill is ready for commercial/non-commercial use.

## Publisher:

[matiasedgeandnode](https://clawhub.ai/user/matiasedgeandnode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, configure, and run the Ampersend CLI so agents can make x402 stablecoin payments within user-defined spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables agents to make real stablecoin payments within configured limits.

Mitigation: Use tight per-transaction, daily, and monthly spending limits; avoid auto-topup unless it is explicitly needed and understood.

Risk: Paid fetches can spend funds when payment requirements are accepted.

Mitigation: Run `ampersend fetch --inspect` before paid requests to review cost and payment requirements without executing payment.

Risk: Private agent keys can be exposed if pasted into commands, logs, or agent transcripts.

Mitigation: Prefer the browser approval flow, avoid sharing private keys with the agent, and rotate any key that was already exposed.

Risk: Dashboard sign-in from an agent-accessible browser could expose account authority.

Mitigation: Have the user make Ampersend dashboard configuration changes directly in their own browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matiasedgeandnode/skills/asndurl)
- [Ampersend staging API endpoint](https://api.staging.ampersend.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON; paid fetches can be inspected before payment.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
