## Description:

投屏控制专业版 helps agents manage Chromecast devices on a local network, including discovery, multi-device and group casting, playback queues, scheduled actions, and status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to guide local-network Chromecast management for signage, classrooms, smart homes, and other multi-device media environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to discover and control real Chromecast devices on a local network.

Mitigation: Use it only when local device control is intended, and require explicit confirmation before cast-to-all, group cast, monitoring, scheduled stop, or stop-all actions.

Risk: The manifest includes broad project-management and collaboration trigger text that does not match the Chromecast control behavior.

Mitigation: Do not activate this skill for project management, task planning, progress tracking, collaboration, or personnel evaluation requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/chromecast-control-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command examples plus JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local-network Chromecast control actions that should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
