## Description:

Consul CLI command reference for service discovery, key-value store, health checks, cluster management, and service mesh operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasgao](https://clawhub.ai/user/jonasgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill as a Consul CLI reference for agent management, key-value operations, service registration, ACL workflows, cluster operations, snapshots, and service mesh commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents high-impact Consul administration commands, including destructive, remote-exec, network-exposing, backup, restore, delete, watch, and exec operations.

Mitigation: Require human review of targets, selectors, backups, command scope, and execution context before running generated commands.

Risk: The skill references ACL SecretIDs, Consul tokens, keyring values, and credential-like values used in cloud auto-join or Consul administration workflows.

Mitigation: Treat these values as secrets and avoid exposing them in logs, shell history, shared prompts, generated output, or public artifacts.

Risk: The skill includes examples that expose Consul on broad network interfaces such as 0.0.0.0.

Mitigation: Bind Consul only to intended interfaces and use authentication, TLS, firewalling, and access controls before exposing network services.

## Reference(s):

- [Consul CLI Reference](references/cli-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, HCL, and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference content for human-reviewed Consul CLI command generation; no automated execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
