## Description:

ClawOrchestrate dispatches tasks to OpenClaw agents on remote machines through a lightweight HTTP dispatcher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loop-capital](https://clawhub.ai/user/loop-capital)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send tasks to agents across multiple trusted machines, monitor basic health, and install a persistent dispatcher service for OpenClaw orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reachable dispatcher can start local OpenClaw agents under the dispatcher's user permissions.

Mitigation: Run the dispatcher only on trusted private networks, bind it to a private or Tailscale interface, and avoid exposing port 9876 broadly.

Risk: Weak or missing authentication can allow unauthorized task dispatch.

Mitigation: Require a strong non-default API key, avoid the broadcast script's fallback key, and pass the key securely to any persistent service configuration.

Risk: Plain HTTP transport can expose dispatch requests on networks that are not identity-aware or private.

Mitigation: Prefer TLS or an identity-aware private transport, and use Tailscale or equivalent network controls for host access.

Risk: Persistent service setup can keep an unsafe dispatcher running after reboot if deployment settings are incomplete.

Mitigation: Fix and review the service configuration, including bind address and API key handling, before enabling persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loop-capital/skills/claworchestrate)
- [Publisher profile](https://clawhub.ai/user/loop-capital)
- [ClawStudio](https://clawstudio.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON request examples, and script or service configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and network access between the gateway and trusted OpenClaw hosts.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
