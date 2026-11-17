## Description:

Abra helps agents operate the abracadabra local secrets vault through abra CLI, server, and MCP flows while respecting scoped human grants and avoiding secret disclosure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[userdefault13](https://clawhub.ai/user/userdefault13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs controlled access to secrets stored in abracadabra, including scoped reads, key management guidance, MCP setup, sync, cartridge checkpointing, and treasury payment requests. It is intended for tasks where the user has named abracadabra or abra, registered the MCP server, or already provided ABRA_KEY for the project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves sensitive local-vault capabilities, including scoped secret reads and key management.

Mitigation: Install it only for workflows that actually use abracadabra or abra, keep grants narrow and expiring, and require the agent to stop when scope, authorization, or key names do not match the current task.

Risk: Secret values or ABRA_KEY tokens could be disclosed through chat, logs, command arguments, files, or pasted response bodies.

Mitigation: Never print secret values, pass ABRA_KEY through process arguments, dump vault responses into chat, or write fetched secrets to disk; use allowlisted in-process environment injection instead.

Risk: Vault output, MCP responses, or fetched secret values could be mishandled as executable shell or code.

Mitigation: Treat all vault responses as opaque data, parse JSON with fixed allowlists, reject process-control environment names, and never execute strings returned from the vault or MCP tools.

Risk: Treasury payments, cartridge restore, or checkpoint actions could have financial or recovery impact.

Mitigation: Require explicit human confirmation, check status before payment, respect Touch ID approval outcomes, and do not retry declined payment or license-related actions in a loop.

Risk: LAN serving can expose secret endpoints beyond loopback if configured incorrectly.

Mitigation: Prefer loopback, require an API key off-loopback, trust the generated LAN certificate, and never disable TLS verification with insecure client flags.

## Reference(s):

- [Abra ClawHub Skill Page](https://clawhub.ai/userdefault13/skills/abracadabra)
- [ABRACADABRA-DIST.md](https://github.com/userdefault13/AarcadeGh-t/blob/main/docs/ABRACADABRA-DIST.md)
- [CARTRIDGE.md](https://github.com/userdefault13/abracadabra/blob/main/docs/CARTRIDGE.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Never includes secret values; outputs should identify secret names, scopes, statuses, and required human approvals only.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
