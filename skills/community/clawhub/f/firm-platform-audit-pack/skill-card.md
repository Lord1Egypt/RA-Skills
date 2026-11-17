## Description:

Platform alignment audit pack for OpenClaw 2026.2 covering Secrets v2, agent routing, voice security, trust model, autoupdate, plugin SDK, content boundaries, and sqlite-vec.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform engineers use this skill to audit OpenClaw 2026.2 configuration files for migration readiness, routing policy, trust model, voice security, autoupdate, plugin SDK, content boundary, and sqlite-vec alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external OpenClaw audit tooling that is not bundled with the artifact.

Mitigation: Confirm the mcp-openclaw-extensions dependency is installed from a trusted source before using the skill.

Risk: Audit commands may inspect sensitive OpenClaw configuration files.

Mitigation: Run checks only on configuration files the user intends to audit.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with YAML and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcp-openclaw-extensions >= 3.0.0 and OpenClaw >= 2026.2; operates on user-provided configuration paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
