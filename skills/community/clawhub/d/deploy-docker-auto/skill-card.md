## Description:

Automates the build, push, remote Docker deployment, and health verification workflow for TPAIP releases on Linux servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lky115](https://clawhub.ai/user/lky115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to deploy TPAIP application updates or fixes by building a Docker image, pushing it to a registry, replacing the remote container, and checking service health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact production deployment actions, including stopping and replacing a running container.

Mitigation: Require final approval of the exact deployment commands and prepare rollback or blue-green deployment before stopping the current container.

Risk: Untrusted deployment values, SSH key paths, or environment-file details could expose secrets or direct commands to the wrong target.

Mitigation: Use only trusted deployment values and keep SSH keys and .env contents out of logs and chat.

Risk: Mutable Docker tags can make deployments hard to reproduce or roll back.

Mitigation: Pin Docker images by immutable tag or digest.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lky115/skills/deploy-docker-auto)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces step-by-step deployment guidance; command parameters must be supplied from trusted user input.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
