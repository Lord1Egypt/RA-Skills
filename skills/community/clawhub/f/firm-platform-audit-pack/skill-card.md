## Description: <br>
Platform alignment audit pack for OpenClaw 2026.2 covering Secrets v2, agent routing, voice security, trust model, autoupdate, plugin SDK, content boundaries, and sqlite-vec. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and platform engineers use this skill to audit OpenClaw 2026.2 configuration for Secrets v2 migration, routing policy, voice security, trust model configuration, autoupdate settings, plugin SDK compliance, content boundary enforcement, and sqlite-vec setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit depends on mcp-openclaw-extensions and reads user-supplied configuration paths. <br>
Mitigation: Confirm the extension package is trusted and run audit commands only against configuration files intended for review. <br>
Risk: The artifact notes that generated content requires human validation before use. <br>
Mitigation: Review audit findings and any resulting configuration changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-platform-audit-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on OpenClaw >= 2026.2 and mcp-openclaw-extensions >= 3.0.0.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
