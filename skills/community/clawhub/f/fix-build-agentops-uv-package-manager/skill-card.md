## Description:

Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Python projects, manage dependencies and virtual environments, migrate from pip, pip-tools, or Poetry workflows, and optimize CI, Docker, and lockfile-based Python development with uv.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quick-install examples can execute remote installer scripts in a workstation or build environment.

Mitigation: Review installer contents before use, prefer package-manager installation where practical, and verify checksums or signatures when available.

Risk: CI and container examples may import mutable external code through version tags or latest container references.

Mitigation: Pin GitHub Actions to immutable commits, pin container images by digest, and review updates before changing pins.

Risk: Dependency and tool updates can alter a project's supply-chain state.

Mitigation: Use committed lockfiles, frozen installs, pinned Python versions, and review lockfile diffs before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/fix-build-agentops-uv-package-manager)
- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [uv Guides](https://docs.astral.sh/uv/guides/)
- [uv pip Compatibility](https://docs.astral.sh/uv/pip/compatibility/)
- [Astral Blog](https://astral.sh/blog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, TOML, YAML, Dockerfile, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command and configuration examples for Python project setup, dependency management, virtual environments, CI, Docker, lockfiles, migration, and troubleshooting.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
