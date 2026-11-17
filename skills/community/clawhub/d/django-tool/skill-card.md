## Description:

Automates setup for Django or Django REST Framework projects with environment provisioning, dependency installation, and starter project files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moenassi](https://clawhub.ai/user/moenassi)

### License/Terms of Use:


## Use Case:

Developers and backend teams use this skill to bootstrap consistent Django or Django REST Framework projects and reduce repeated manual setup work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that ordinary project names, app names, paths, or model names can cause unintended shell command execution.

Mitigation: Run only in a disposable directory or isolated environment, avoid untrusted names and paths, and prefer a revised version that validates Django identifiers and uses subprocess argument lists or Python file APIs.

Risk: The release has no declared license in the provided evidence.

Mitigation: Confirm the license and terms of use before installation, redistribution, or commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moenassi/skills/django-tool)
- [Publisher profile](https://clawhub.ai/user/moenassi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Interactive command-line guidance and generated Django project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project scaffolding based on user-provided path, project name, app name, setup mode, and optional model names.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
