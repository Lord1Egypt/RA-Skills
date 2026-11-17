## Description:

Downloads Docker images from registries and packages them as tar files for offline docker load use, with SOCKS5 proxy and mirror-based download modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaohaixin](https://clawhub.ai/user/zhaohaixin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to fetch Docker images for offline transfer or environments where direct docker pull access is unreliable. It helps configure proxy or mirror download settings, choose a target architecture, run the pull workflow, and report the generated tar path and docker load command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry credentials or private registry details could be exposed through command-line arguments or debug output.

Mitigation: Avoid passing registry passwords on the command line and avoid debug mode when working with private registries.

Risk: Downloaded image content may be untrusted or altered before it is loaded into Docker.

Mitigation: Verify downloaded images independently before loading or running them.

Risk: Mirror-mode execution uses shell-style pipelines with configuration-derived values.

Mitigation: Review or update the mirror-mode execution path so it avoids shell pipelines with interpolated configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaohaixin/skills/docker-image-puller)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown or plain text status reports with inline shell commands and generated Docker image tar paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs produce Docker image tar archives intended for docker load.]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
