## Description:

Automatically creates a ready-to-use Django or Django REST Framework project with preconfigured settings and environment provisioning for faster backend project setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moenassi](https://clawhub.ai/user/moenassi)

### License/Terms of Use:


## Use Case:

Developers and backend teams use this skill to bootstrap Django or Django REST Framework projects with a consistent starting structure, isolated environment setup, dependencies, and initial app configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-entered paths and names are used in local shell commands, which can execute unintended commands or modify unexpected local files.

Mitigation: Review before installing or running; use only in a disposable directory with trusted inputs, and replace shell-string calls with subprocess argument lists plus input validation.

Risk: Project scaffolding writes and rewrites Django files during setup, which can overwrite expected local configuration if run in the wrong location.

Mitigation: Confirm target paths before execution, add overwrite confirmations, and prefer pathlib-based path handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moenassi/skills/django-creator)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration]

**Output Format:** [Generated Django project files and terminal-driven setup output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive prompts collect project path, project name, app name, setup mode, and model names.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
