## Description:

Automates guided Ubuntu workstation setup for algorithm and deep learning development, including system checks, development tool installation, Docker, Conda, CUDA/cuDNN, shell configuration, and China-optimized network mirrors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize or reset Ubuntu algorithm development workstations and install common deep learning, container, GPU, editor, browser, and terminal tooling through step-by-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent system, package, shell, Docker, CUDA, and global Git or environment changes can affect the workstation beyond a single project.

Mitigation: Review each step before execution, run on a backed-up or disposable workstation when possible, and prefer per-project configuration for proxy and environment settings.

Risk: Installer patterns and externally supplied package, mirror, or environment URLs can introduce untrusted code or packages.

Mitigation: Use official signed repositories, pinned versions, and trusted URLs; avoid HTTP installers, direct curl-to-shell patterns, and untrusted DEB, mirror, or environment JSON inputs.

## Reference(s):

- [Configuration Templates](references/config_templates.md)
- [CUDA and cuDNN Installation Guide](references/cuda_guide.md)
- [Ubuntu Development Tools Guide](references/tools_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/jessy-huang/skills/eai-dev-setup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output should prompt for confirmation before sudo, persistent configuration, package installation, or reboot-related actions.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
