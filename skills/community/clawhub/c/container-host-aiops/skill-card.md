## Description:

Govern Docker, Portainer, and Podman container hosts with read operations, diagnostic analyses, and guarded management actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect a single Docker, Portainer, or Podman host, diagnose container and resource problems, and carry out approved host changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A read-only Docker socket mount can still permit destructive actions.

Mitigation: Enforce API restrictions with an authorization plugin, filtering proxy, or restricted Portainer account.

Risk: Destructive container-management calls and volume pruning can cause service disruption or data loss.

Mitigation: Require agent-client approval for destructive MCP calls, review dry-run previews, and back up important volumes before pruning. Keep TLS verification enabled.

## Reference(s):

- [Project homepage](https://github.com/AIops-tools/Container-Host-AIops)
- [ClawHub release page](https://clawhub.ai/zw008/skills/container-host-aiops)
- [Capabilities reference](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Structured JSON tool results and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected host operation and may include diagnostic findings, recommendations, previews, or action outcomes.]

## Skill Version(s):

0.14.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
