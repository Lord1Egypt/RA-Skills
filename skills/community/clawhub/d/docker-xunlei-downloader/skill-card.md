## Description:

Interact with Docker-deployed Xunlei services to submit magnet links, monitor download tasks, and prioritize main content downloads with filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saaak](https://clawhub.ai/user/saaak)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to control a Docker-deployed Xunlei service from an agent, including configuring the service endpoint, submitting magnet downloads, and checking active or completed tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real remote download tasks with visible metadata and resource usage.

Mitigation: Use it only with a Xunlei service you control and review each submit command before execution.

Risk: The bundled configuration defaults to plaintext HTTP and includes an environment-specific service address.

Mitigation: Replace config.json with local settings and prefer HTTPS or an isolated trusted network.

Risk: The release depends on request libraries flagged by the security summary.

Mitigation: Update or pin dependencies from an approved registry before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saaak/skills/docker-xunlei-downloader)
- [Xunlei Docker service project](https://github.com/cnk3x/xunlei)
- [Artifact README](artifact/README.md)
- [Artifact configuration guide](artifact/CONFIG.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style text responses with command examples and task status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger remote Xunlei service API calls that create, inspect, or report download tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
