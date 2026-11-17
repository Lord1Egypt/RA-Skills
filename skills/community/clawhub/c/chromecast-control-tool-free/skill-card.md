## Description:

投屏控制免费版 helps an agent guide Chromecast device discovery, URL or local media casting, playback controls, volume changes, and status checks using catt commands on a trusted local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Chromecast devices from an agent workflow on the same local network, including scanning for devices, casting media, controlling playback, adjusting volume, and checking device status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill can route broad casting and playback commands to local-network devices.

Mitigation: Install only when Chromecast control through catt is intended, and review proposed commands before execution.

Risk: Casting local files or internal URLs may expose sensitive content to a Chromecast device or anyone viewing it.

Mitigation: Use the skill only on trusted local networks and avoid casting sensitive local files, private URLs, or internal resources.

Risk: The artifact includes inconsistent API-key and HTTPS safety claims even though the core workflow says it uses local catt commands without cloud authentication.

Mitigation: Do not rely on those safety claims as written; verify the actual command path, dependencies, and network behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chromecast-control-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and occasional JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before command execution because the skill can affect local-network Chromecast devices and cast local files or URLs.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
