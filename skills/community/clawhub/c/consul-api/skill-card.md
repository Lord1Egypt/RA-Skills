## Description:

Consul HTTP API operations for service discovery, key-value store, health checks, and service mesh management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasgao](https://clawhub.ai/user/jonasgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to look up Consul HTTP API patterns for service discovery, KV storage, health checks, ACL token operations, sessions, transactions, and service mesh configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents Consul operations that can change cluster state, including deletes, ACL changes, service registration, and service mesh intentions.

Mitigation: Require explicit confirmation for destructive or access-changing operations, and verify the datacenter, namespace, service, and key prefix before using an example against a real cluster.

Risk: Consul ACL tokens may be exposed if copied into shared prompts, logs, command history, or transcripts.

Mitigation: Use least-privilege ACL tokens, avoid management tokens, redact credentials from examples, and keep real tokens out of shared agent conversations.

## Reference(s):

- [Complete API endpoint reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/jonasgao/skills/consul-api)
- [Publisher profile](https://clawhub.ai/user/jonasgao)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline HTTP examples, JSON snippets, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-oriented responses may include Consul endpoint paths, query parameters, request bodies, and operational cautions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
