## Description:

A general AI agent cloning skill for exporting, validating, and importing configuration packages with ZIP Slip protection, metadata redaction, and sensitive-file exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srchengtao2025](https://clawhub.ai/user/srchengtao2025)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to back up an AI agent workspace, transfer configuration between agents, or restore agent identity, memory, tool, and workflow files from a ZIP package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clone packages may contain sensitive agent identity, memory, tool configuration, or private workspace files.

Mitigation: Inspect package contents before sharing or import, scan for secrets and private memory, use the documented exclusion options, and encrypt packages during transfer.

Risk: Importing a clone package can overwrite existing target workspace files.

Mitigation: Back up the target workspace, preview the package before import, avoid --force for routine use, and test imports in an isolated workspace first.

Risk: Untrusted clone packages can introduce unwanted or unsafe agent configuration.

Mitigation: Use packages only from trusted sources and run the included verify command before importing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/srchengtao2025/skills/aicone)
- [Publisher profile](https://clawhub.ai/user/srchengtao2025)
- [AI Clone README](README.md)
- [AI agent cloning best practices](references/best-practices.md)
- [Machine Cat clone configuration](references/machine-cat-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated ZIP configuration packages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included Python script can create, inspect, and import ZIP packages containing agent workspace configuration files.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
