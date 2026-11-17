## Description:

Diagnose and fix R environment issues, including package installation failures, dependency conflicts, system library problems, renv errors, and Bioconductor version mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:


## Use Case:

Developers, data scientists, and R project maintainers use this skill to diagnose and repair R package installation failures, dependency conflicts, renv issues, Bioconductor mismatches, missing system libraries, compiler problems, PATH issues, and permission problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended commands may change R libraries, project lockfiles, PATH or permission settings, or install system packages.

Mitigation: Review sudo, dnf, apt, brew, renv restore/update, PATH, and permission changes before approval, especially on shared or production machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackkuo666/skills/debugging-r-environment-and-dependencies)
- [Artifact README](artifact/README.md)
- [Examples overview](artifact/examples/README.md)
- [Missing system dependencies demo](artifact/examples/missing-system-deps/README.md)
- [Broken renv project demo](artifact/examples/broken-renv-project/README.md)
- [Bioconductor version mismatch demo](artifact/examples/bioc-version-mismatch/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with R, shell, and configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OS-specific package manager commands and R package-management steps.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
