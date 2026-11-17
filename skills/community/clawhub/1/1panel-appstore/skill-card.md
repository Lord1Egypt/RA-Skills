## Description:

Create 1Panel appstore/local-app installation packages for Dockerized applications from official repositories, Docker images, docker-compose.yml files, or a prepared app spec.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1panel](https://clawhub.ai/user/1panel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert Dockerized applications, official Docker Compose setups, Docker images, or prepared app specs into 1Panel App Store local app packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated packages may include executable init.sh content derived from app specs.

Mitigation: Review generated scripts/init.sh and confirm each action is backed by official source evidence before placing the package in 1Panel.

Risk: Untrusted prepared specs can influence docker-compose.yml, YAML metadata, mounts, and service settings.

Mitigation: Use official sources or trusted specs only, then review generated Compose files for privileged mode, host networking, namespace sharing, Docker socket mounts, root or system mounts, and unpinned images.

Risk: Incorrect Docker source details can produce misleading or unsafe app packages.

Mitigation: Confirm Docker images, ports, volumes, environment variables, runtime users, and init actions against the application owner repository or official documentation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1panel/skills/1panel-appstore)
- [Source Policy](artifact/references/source-policy.md)
- [1Panel Appstore Format](artifact/references/appstore-format.md)
- [Intermediate App Spec](artifact/references/appspec.md)
- [Review Checklist](artifact/references/review-checklist.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration]

**Output Format:** [1Panel app package files, including Markdown READMEs, YAML app metadata, docker-compose.yml, optional shell initialization scripts, and summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; generated packages should be reviewed before placement in 1Panel.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
