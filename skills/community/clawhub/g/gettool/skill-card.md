## Description:

Fetches and installs C++ tools and libraries from a cpp_tools repository, including listing, cloning, optional CMake builds, installation scripts, version checkout, and repository URL management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to fetch, clone, build, and install third-party C++ libraries such as eigen, opencv, pcl, fmt, and spdlog into local project directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch C++ source code and run build or install commands from configurable repositories.

Mitigation: Use pinned trusted sources and run builds in a contained, non-privileged environment.

Risk: The documented global install option can invoke privileged installation behavior.

Mitigation: Avoid --global-install-flag unless the repository and installation scripts have been manually verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/gettool)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and command options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that fetch, build, or install source code from configurable repositories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
