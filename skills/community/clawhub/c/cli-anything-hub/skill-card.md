## Description:

Discover agent-native CLIs for professional software. Access the live catalog to find tools for creative workflows, productivity, AI, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuh-yang](https://clawhub.ai/user/yuh-yang)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to discover CLI-Anything tools and produce commands for browsing, installing, and running agent-native command-line interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to install unpinned packages from a mutable live catalog.

Mitigation: Review package names, versions, sources, and maintainer trust before installation, and run installs only in disposable or least-privileged environments.

Risk: Catalog-suggested commands could run in a workspace that contains sensitive files or credentials.

Mitigation: Require explicit approval before executing install commands and avoid running them in sensitive workspaces.

## Reference(s):

- [Live CLI-Hub Catalog](https://clianything.cc/SKILL.txt)
- [CLI-Anything Web Hub](https://clianything.cc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a mutable live catalog and package install commands that require review before execution]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
