## Description:

AssetClaw helps agents work with AssetHub asset lifecycle workflows, including asset lookup, maintenance requests, approvals, inventory, procurement, retirement, compliance, IoT monitoring, documents, spare parts, labels, alerts, and related API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmu4hlee](https://clawhub.ai/user/cmu4hlee)

### License/Terms of Use:

MIT-0

## Use Case:

AssetHub users and asset operations teams use this skill to query asset records, prepare or execute authorized AssetHub API calls, and manage operational workflows such as repair, transfer, procurement, inspection, compliance, labels, and IoT monitoring. It is intended for environments with an existing AssetHub deployment and authorized credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can handle credentials and session data in local temporary files.

Mitigation: Use a dedicated low-privilege AssetHub account, prefer environment or managed secret injection over prompt-supplied passwords, and remove session files on logout or after use.

Risk: The skill covers high-impact administrative and write operations such as asset deletion, role changes, backup or restore, service-token, and system configuration actions.

Mitigation: Review the exact endpoint and payload before execution, query the target object before writes, require explicit confirmation for high-risk replays, and route sensitive changes through normal administrative approval where possible.

Risk: Reusing an idempotency key with a different payload can create conflicts or unsafe retry behavior.

Mitigation: Use a stable idempotency key only for one intended request body and generate a new key for different payloads.

Risk: Cross-tenant AssetHub operations can affect the wrong tenant when elevated accounts are used.

Mitigation: Use the tenant returned by the authorized session unless a verified administrative workflow explicitly requires another tenant, and confirm tenant context before writes.

Risk: Non-HTTPS or unreviewed endpoints can expose credentials or operational data.

Mitigation: Prefer HTTPS AssetHub endpoints and review the configured API URL before login or write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cmu4hlee/skills/assetclaw)
- [AssetHub website](http://www.medfix.cn)
- [AssetClaw skill documentation](artifact/SKILL.md)
- [AssetHub API Top 40 quick reference](artifact/references/endpoint-quick-ref.md)
- [Authentication and workflow reference](artifact/references/auth-and-workflows.md)
- [AssetHub API modules overview](artifact/references/api-modules-overview.md)
- [AssetHub API domain map](artifact/references/api-domain-map.md)
- [Asset state machine](artifact/references/asset-state-machine.md)
- [API conventions](artifact/references/api-conventions.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON payloads]

**Output Format:** [Markdown guidance with bash or curl commands and JSON request or response examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution requires an AssetHub API endpoint and authorized credentials; outputs should not expose passwords, tokens, or tenant secrets.]

## Skill Version(s):

1.7.0 (source: server release evidence and artifact changelog, released 2026-07-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
