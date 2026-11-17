## Description:

Connect OpenClaw to the FTTR Copilot cloud-control system through ConnectRPC for device lookup, alert triage, network diagnostics, and FTTR operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fttrai](https://clawhub.ai/user/fttrai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support engineers use this skill to query customer-authorized FTTR Copilot cloud data, review device status and alerts, run network diagnostics, and perform documented FTTR operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a customer bearer token and request data to the configured FTTRAI_RPC_URL endpoint.

Mitigation: Keep FTTRAI_RPC_URL on the official HTTPS endpoint unless a custom endpoint has been separately verified, and use the least-privileged FTTRAI token available.

Risk: The skill can read customer-bound device details, alerts, topology, metrics, and raw backend responses.

Mitigation: Install only for trusted users and environments authorized to access the relevant customer FTTR data.

Risk: The skill can update device aliases and issue documented real-time information commands.

Mitigation: Review requested operations before execution and use account or token permissions scoped to the intended devices and operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fttrai/skills/fttr-copilot)
- [FTTR Copilot ConnectRPC default endpoint](https://fms-main.fttrai.com/api)
- [Artifact README](artifact/README.md)
- [Usage examples](artifact/examples/usage.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON from the bundled CLI, with agent-facing summaries and diagnostic guidance derived from customer-authorized FTTR Copilot responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an FTTRAI_AUTH_TOKEN; FTTRAI_RPC_URL, FTTRAI_TIMEOUT_MS, and FTTRAI_MAX_RETRIES are configurable.]

## Skill Version(s):

0.1.6 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
