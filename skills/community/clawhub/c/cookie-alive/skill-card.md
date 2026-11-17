## Description:

Persists, refreshes, and serves website session cookies through a local SQLite-backed cookie store for scheduled keepalive requests and downstream Cookie header or JSON cookie map use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage authenticated website session cookies without browser automation, keeping named profiles refreshed and available to local programs as Cookie headers, JSON maps, or records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and serves live login cookies, so exposed database files or printed cookie values can grant access to the corresponding accounts.

Mitigation: Treat the skill as a local credential store, protect ~/.cookie_alive, restrict access to trusted local programs, and avoid logging or sharing cookie outputs.

Risk: The optional HTTP wrapper can expose cookies over a local HTTP endpoint if run without additional safeguards.

Mitigation: Avoid the HTTP wrapper unless authentication is added and the server remains loopback-only.

Risk: HTTP refresh URLs can transmit session cookies without transport encryption.

Mitigation: Use trusted sites and HTTPS refresh URLs whenever possible; avoid HTTP refresh URLs.

## Reference(s):

- [Command Reference](references/commands.md)
- [ClawHub Skill Page](https://clawhub.ai/seanmwx/skills/cookie-alive)
- [Publisher Profile](https://clawhub.ai/user/seanmwx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON or Cookie header outputs from the runtime scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce local SQLite-backed session records and can print live cookie values; downstream handling should treat these outputs as credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
