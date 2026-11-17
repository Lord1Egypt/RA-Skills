## Description:

Protect sensitive environment variables from accidental exposure in commits, logs, and CI pipelines with automated scanning and pre-commit validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit repositories, staged changes, environment files, and CI/CD workflows for exposed secrets or unsafe environment-variable handling. It also provides remediation guidance such as moving secrets to environment variables, rotating leaked credentials, updating .gitignore entries, and adding pre-commit or CI scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret scan output may reveal sensitive file paths or locations where credentials appear.

Mitigation: Keep scan output private, review findings locally, and avoid publishing logs that include sensitive paths or values.

Risk: Suggested .gitignore, hook, or CI/CD changes may affect repository workflow if applied automatically.

Mitigation: Review proposed changes before applying them and test pre-commit or CI behavior on a small change first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/flyai-env-guardian)
- [Publisher profile](https://clawhub.ai/user/dingtom336-gif)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with findings, remediation steps, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify sensitive file paths or secret locations in scan output; review before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
