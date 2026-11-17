## Description:

Code Quality Guardian detects code smells, complexity issues, security vulnerabilities, and style violations across Python, JavaScript/TypeScript, and Go projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to analyze source repositories, surface code quality and security findings, and generate reports for local review or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports may embed untrusted scan output without escaping when analyzing untrusted repositories.

Mitigation: Run the skill in an isolated, minimally privileged environment and prefer console or JSON output until HTML escaping is reviewed.

Risk: Dependency ranges may change installed scanner behavior in CI.

Mitigation: Use a reviewed lockfile or pinned requirements before deploying the skill in CI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/code-quality-guardian)
- [Project homepage](https://github.com/kaiyuelv/code-quality-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples and generated console, JSON, HTML, or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files when an output path is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
