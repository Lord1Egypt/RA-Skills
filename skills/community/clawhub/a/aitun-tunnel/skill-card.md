## Description:

Expose local web pages and HTTP services to the public internet via secure tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to share locally running web pages, dashboards, HTTP services, webhook endpoints, and APIs through public tunnel URLs for review, demos, and integration testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party tunneling tool can make chosen local services publicly reachable.

Mitigation: Use it only for services intended to be shared, avoid sensitive local endpoints, and stop the tunnel or daemon when sharing is no longer needed.

Risk: Installer commands such as curl-to-bash or irm-to-iex can execute remote code directly.

Mitigation: Prefer the documented pip or uv install path and review package source or provenance where possible before installation.

Risk: Forwarding administrative, debug, database, SSH, or RDP ports can expose sensitive systems.

Mitigation: Avoid forwarding privileged or sensitive ports and limit tunnels to the specific local HTTP service needed for the task.

## Reference(s):

- [AiTun Homepage](https://aitun.cc)
- [ClawHub Skill Page](https://clawhub.ai/ctz168/skills/aitun-tunnel)
- [ClawHub Metadata Link](https://clawhub.ai/ctz168/aitun-tunnel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public tunnel URLs and cleanup commands for the selected local service.]

## Skill Version(s):

4.0.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
