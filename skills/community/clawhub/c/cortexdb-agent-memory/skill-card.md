## Description:

Gives a Node.js agent durable local memory, semantic or lexical recall, and a queryable SPARQL knowledge graph through CortexDB and the cortexdb-client package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliang-cn](https://clawhub.ai/user/liliang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add durable user memory, knowledge retrieval, and graph-backed relationship queries to OpenClaw or other Node.js agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists user memories and knowledge in a local CortexDB sidecar, which can retain sensitive user data beyond the current session.

Mitigation: Define clear rules for what may be remembered, obtain appropriate consent, and provide a process for reviewing and deleting stored data.

Risk: The helper connects to a gRPC endpoint using bearer-token authentication, and the skill notes plaintext localhost transport.

Mitigation: Use a strong generated token, keep the endpoint bound to localhost, and configure TLS or a reverse proxy before cross-machine access.

Risk: The integration depends on the CortexDB sidecar binary and the cortexdb-client npm package.

Mitigation: Use pinned dependency versions and review the sidecar and package before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liliang-cn/skills/cortexdb-agent-memory)
- [cortexdb-client npm package](https://www.npmjs.com/package/cortexdb-client)
- [CortexDB project documentation](https://github.com/liliang-cn/cortexdb)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent integration guidance and helper tool functions for remembering, recalling, storing knowledge, relating entities, and querying SPARQL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
