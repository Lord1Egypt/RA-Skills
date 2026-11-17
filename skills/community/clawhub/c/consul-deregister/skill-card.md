## Description:

Deregisters Consul service instances via the Consul HTTP API, supporting service ID batches, replayed curl deregistration commands, dry-run previews, parallel execution, and ACL token authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strongant](https://clawhub.ai/user/strongant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to preview and execute Consul service deregistration across one or more Consul agents during removals, rollbacks, or migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live batch deregistration can remove service registrations from multiple Consul agents.

Mitigation: Use dry-run first and require human confirmation before live deregistration.

Risk: ACL tokens may be exposed or sent to untrusted Consul agent addresses.

Mitigation: Use only trusted HTTPS agent URLs, avoid command-line tokens where possible, and use narrowly scoped Consul ACL tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/strongant/skills/consul-deregister)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script supports dry-run previews, batch execution, ACL token authentication, and non-zero exit status when any deregistration fails.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
