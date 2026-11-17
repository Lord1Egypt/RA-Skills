## Description:

Installs and activates @bowong/clawshow-gateway in OpenClaw, then migrates existing Gateway channel configuration to ClawShow with rollback safety and no default outbound test traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yudi-xiao](https://clawhub.ai/user/yudi-xiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install the ClawShow gateway plugin for OpenClaw and migrate an existing Gateway channel configuration while preserving unrelated settings and creating rollback coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migrated ClawShow channel enables allowFrom ["*"], which permits public relay access if deployed as written.

Mitigation: Use an explicit allowlist unless public relay access is intentional.

Risk: The workflow handles CLAWSHOW_AUTH_TOKEN and token-bearing gateway configuration.

Mitigation: Avoid exposing full token-bearing config on the command line when safer input methods exist, and protect or delete secret-bearing backups when they are no longer needed.

Risk: The workflow installs @bowong/clawshow-gateway and ws during migration.

Mitigation: Pin reviewed package and plugin versions where possible before use in environments with meaningful tool access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yudi-xiao/skills/clawshow-gateway-connect)
- [Publisher profile](https://clawhub.ai/user/yudi-xiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup path and verification command results when available.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
