## Description:

DeerFlow 2.0 installation and configuration guidance for OpenClaw environments, covering repository setup, dependency installation, configuration, service startup, validation, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangbb-coder](https://clawhub.ai/user/fangbb-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, run, and troubleshoot DeerFlow 2.0 in OpenClaw environments. It provides command guidance, configuration examples, startup checks, and common issue resolutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run mutable third-party installation code and Make targets from the DeerFlow upstream repository.

Mitigation: Review the cloned repository first and pin the upstream commit or release before running installation commands.

Risk: Docker-level privileges, shell access, and file-write tools can broaden the impact of mistakes or compromised dependencies.

Mitigation: Use a dedicated low-privilege account or rootless Docker, restrict sandbox paths, and enable only the tools required for the deployment.

Risk: API keys are stored in environment configuration and services are started in the background.

Mitigation: Protect secret files, avoid committing credentials, document service stop and cleanup steps, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/fangbb-coder/skills/deerflow-install-master)
- [DeerFlow upstream project homepage](https://github.com/bytedance/deer-flow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, env, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation reports, troubleshooting checklists, API examples, and startup script guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
