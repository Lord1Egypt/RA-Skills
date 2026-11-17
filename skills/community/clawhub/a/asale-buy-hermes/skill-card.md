## Description:

Switch Hermes between buying from the asale market and using its own subscription, and see which running sessions are still on the old config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route Hermes through asale's local buying proxy, restore Hermes to its own subscription, and identify running Hermes sessions that have not picked up the new configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install and update path runs remote scripts from asale.ai directly in a shell.

Mitigation: Review the installer before running it, prefer signed or checksum-verified releases, and avoid elevated privileges.

Risk: The skill reads a local daemon token and sends authenticated requests to the loopback daemon.

Mitigation: Keep the token file protected, use loopback-only daemon access, and do not share command logs that include local credentials.

Risk: The skill changes the Hermes configuration used for future sessions.

Mitigation: Run the status check before changing settings, confirm the selected model list, and restart Hermes only when the user chooses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/asale-buy-hermes)
- [asale homepage](https://asale.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a local asale daemon token for authenticated loopback RPC calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
