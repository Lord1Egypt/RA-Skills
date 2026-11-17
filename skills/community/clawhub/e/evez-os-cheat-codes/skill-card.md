## Description:

Provides a reference of OpenClaw, GCP, and EVEZ-OS commands and environment variables for system control, debugging, networking, and advanced operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Experienced OpenClaw and GCP operators use this skill as review-only reference material for locating advanced gateway, agent, environment-variable, networking, and diagnostic controls before applying changes in authorized environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes operations that can expose credentials, disable authentication, capture full traffic or payloads, and grant full host access.

Mitigation: Use the material only in isolated, authorized diagnostic environments, keep device authentication enabled, avoid broad trusted-proxy ranges, minimize retention, and clean up secrets after testing.

Risk: The skill includes MCP package setup commands that could introduce unreviewed third-party tools.

Mitigation: Pin and review MCP packages before enabling them in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-os-cheat-codes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; commands and settings require human review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
