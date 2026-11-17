## Description:

Install and use ClawPolicy, an explainable autonomous execution policy engine for low-touch, auditable agent execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzming](https://clawhub.ai/user/dzming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install ClawPolicy, initialize local policy storage, inspect policy lifecycle status, and access its CLI and Python API for auditable agent execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the current unpinned PyPI clawpolicy package under the user's account.

Mitigation: Pin the intended package version, for example clawpolicy==3.0.1, and review the package before use.

Risk: Initialization can create local .clawpolicy/ files that may later guide agent behavior.

Mitigation: Review the generated .clawpolicy/ files before allowing them to influence automated execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dzming/skills/clawpolicy)
- [Upstream English README](references/upstream-README.md)
- [Upstream Changelog](references/upstream-CHANGELOG.md)
- [Upstream Security Policy](references/upstream-SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .clawpolicy/ policy files when the user runs initialization commands.]

## Skill Version(s):

3.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
