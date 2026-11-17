## Description:

Provides setup and usage guidance for a Windows desktop AI assistant with fault tolerance, auto-restart, performance monitoring, voice output, logging, and resource cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk43994](https://clawhub.ai/user/kk43994)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install and run a Windows desktop assistant that integrates with OpenClaw, provides voice notifications, and exposes health, log, and test workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to run unreviewed, unpinned code from GitHub and install npm and Python dependencies that were not included in the reviewed package.

Mitigation: Review the referenced repository, use a trusted commit or signed release, and inspect dependencies before running npm or pip installation commands.

Risk: The app is intended to run continuously, write logs, use a local OpenClaw port, and interact with desktop and voice components.

Mitigation: Run it as a normal user, avoid administrator privileges, prefer an isolated environment, restrict local port exposure, and monitor generated logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kk43994/skills/claw-desktop-pet)
- [Project README](https://github.com/kk43994/claw-desktop-pet#readme)
- [Technical Documentation](https://github.com/kk43994/claw-desktop-pet/tree/master/docs)
- [Release Notes v1.3.0](https://github.com/kk43994/claw-desktop-pet/blob/master/RELEASE-v1.3.0.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, configuration examples, health checks, log inspection commands, and test commands.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact changelog, released 2026-02-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
