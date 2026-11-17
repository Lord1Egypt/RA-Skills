## Description:

Statically audit Dockerfiles for common container hardening risks (root user, unpinned/latest base images, missing healthchecks, and risky build patterns).

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and platform engineers use this skill to review Dockerfiles before release, identify common container hardening gaps, and optionally gate builds when critical findings are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read every file that matches its Dockerfile glob in the current workspace, which can be broad in large or sensitive repositories.

Mitigation: Set DOCKERFILE_GLOB, FILE_MATCH, or FILE_EXCLUDE to narrow the scan to intended Dockerfiles before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/dockerfile-hardening-audit)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text or JSON audit report with ranked Dockerfile findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report can include summary counts, per-Dockerfile severity and score, finding details, and critical Dockerfile lists when JSON output is selected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
