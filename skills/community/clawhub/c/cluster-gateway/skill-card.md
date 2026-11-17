## Description:

Manages the OpenClaw Cluster Gateway as a central hub for sub-agent communication, task distribution, and cluster coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cluster operators use this skill to manage an OpenClaw gateway node for status checks, sub-agent deployment, task dispatch, relay configuration, and cluster role planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes high-impact remote orchestration operations, including sub-agent deployment, task dispatch, and relay configuration.

Mitigation: Use the gateway only on trusted networks with explicit authentication, encrypted transport, least-privilege service accounts, command validation, logging, and approval controls.

Risk: The sample configuration binds the gateway to all interfaces.

Mitigation: Restrict network exposure to approved management interfaces or private networks before using the configuration against a real cluster.

Risk: The messaging interface is marked as pending, so communication behavior and safety boundaries may be incomplete.

Mitigation: Confirm the messaging provider, transport security, alerting, and operational controls before enabling gateway operations.

## Reference(s):

- [Cluster Gateway on ClawHub](https://clawhub.ai/kikikari/skills/cluster-gateway)
- [Publisher profile](https://clawhub.ai/user/kikikari)
- [Worker Node Skill](../worker-node/SKILL.md)
- [Relay Node Skill](../relay-node/SKILL.md)
- [Resource Manager Skill](../resource-manager/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cluster role definitions, command examples, and a sample gateway configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
