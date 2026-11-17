## Description:

Configuration migration and integrity audit pack for shell environment sanitization, plugin integrity, token separation, OpenTelemetry redaction, and RPC rate limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit configuration migrations before rollout, with checks for environment sanitization, plugin manifest drift, token separation, telemetry redaction, and RPC rate limiting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mcp-openclaw-extensions for the actual audit checks.

Mitigation: Confirm the required package is trusted and intentionally installed before using the skill.

Risk: Audit findings can require judgment before configuration migration changes are applied.

Mitigation: Review audit results before making migration changes manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/skills/firm-config-migration-pack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline tool invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on mcp-openclaw-extensions >= 3.0.0 for the actual audit checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
