## Description:

Self-healing China mirror source resolver that discovers, validates, and configures domestic mirror sources for common development tools when downloads are slow or timing out in mainland China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the-ladder-of-rrogress](https://clawhub.ai/user/the-ladder-of-rrogress)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose slow or failed package, source-code, model, and container downloads in mainland China, then select and apply a validated mirror configuration with rollback guidance.

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: The skill can persistently redirect package, source-code, model, and container downloads through third-party mirrors.

Mitigation: Require the agent to show the exact old and new configuration, prefer official or institutional mirrors, and keep rollback commands available before applying changes.

Risk: Using pip trusted-host can bypass TLS certificate verification for the configured host.

Mitigation: Avoid trusted-host unless the user explicitly accepts the TLS trade-off and the mirror is a known institutional or major cloud provider source.

Risk: GitHub accelerators may expose private repository paths or token-bearing URLs to third-party services.

Mitigation: Do not use GitHub accelerators for private repositories, credentialed URLs, or other sensitive source-code access.

Risk: Docker, apt, yum, shell-profile, and persistent environment changes can affect future builds and system package resolution.

Mitigation: Back up existing configuration, merge rather than overwrite structured files, verify after changes, and document rollback steps.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/the-ladder-of-rrogress/skills/china-mirror-resolver)
- [Configuration Templates](references/config-templates.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent development tool and system package source changes after validating candidate mirrors.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
