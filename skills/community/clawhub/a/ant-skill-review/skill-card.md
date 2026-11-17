## Description:

Security scanner for Claude Code Skill packages that audits Skill directories for safety risks before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antaisecuritylab](https://clawhub.ai/user/antaisecuritylab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use Skill Review to audit Claude Code Skill packages before installation, combining deterministic pre-scans with LLM-assisted analysis of prompt injection, malicious behavior, dependencies, and other risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full analysis agent can run broad shell commands while inspecting a target skill.

Mitigation: Run it in an isolated, disposable environment with no sensitive files or credentials, and mount the target skill read-only.

Risk: The deep-analysis tooling can fetch arbitrary external URLs and query package registries.

Mitigation: Restrict network access away from private and internal addresses, allowing only the public package and URL lookups needed for the scan.

Risk: Scanner results depend on Node dependencies and an external LLM provider configuration.

Mitigation: Pin or lock dependencies and configure the LLM API key only inside the isolated scan environment.

## Reference(s):

- [Skill Review on ClawHub](https://clawhub.ai/antaisecuritylab/skills/ant-skill-review)
- [npm registry](https://registry.npmjs.org)
- [PyPI](https://pypi.org)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Human-readable text report or structured JSON security report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 0-5 risk scores, safe/medium/high overall risk, and install/caution/do_not_install recommendation.]

## Skill Version(s):

1.0.2 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
