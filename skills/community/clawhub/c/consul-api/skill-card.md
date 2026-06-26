## Description: <br>
Consul API helps agents provide HTTP API guidance for service discovery, key-value store operations, health checks, ACL token management, and service mesh management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasgao](https://clawhub.ai/user/jonasgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when working with Consul clusters to look up endpoints and draft requests for catalog, KV, health, ACL, agent, session, transaction, and service mesh operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents powerful Consul administrative operations, including writes, deletes, ACL changes, service deregistration, sessions, transactions, and maintenance-related actions. <br>
Mitigation: Require explicit review before applying mutating operations, verify the target datacenter, namespace, key prefix, service, or intention, and use least-privilege ACL tokens. <br>
Risk: Consul examples may include tokens, key values, or operational details that should not be exposed. <br>
Mitigation: Redact secrets and sensitive cluster information before sharing prompts, outputs, logs, or generated commands. <br>


## Reference(s): <br>
- [Consul API Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP endpoint examples, JSON request bodies, and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; outputs should be reviewed before applying changes to a Consul cluster.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
