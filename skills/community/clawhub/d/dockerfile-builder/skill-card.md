## Description:

Generates and lints Dockerfiles for common languages and frameworks to help create container configs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create starter Dockerfiles, lint Dockerfiles for common issues, request optimization suggestions, generate a multi-stage template, and scan a file for secret-like lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shell script can inspect arbitrary file paths and print secret-like lines.

Mitigation: Run it only against intended Dockerfile paths, review file arguments before execution, and avoid scanning sensitive files.

Risk: Shell argument handling can broaden local file access unexpectedly.

Mitigation: Fix the script to use shifted arguments consistently, quote file operands, add -- before grep operands, and validate regular files.

Risk: Secret scanning output can expose matched secret values.

Mitigation: Redact matched values or print only line numbers and finding categories before sharing output.

## Reference(s):

- [Dockerfile Builder ClawHub listing](https://clawhub.ai/ckchzh/skills/dockerfile-builder)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text containing Dockerfile snippets, lint findings, optimization suggestions, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file path arguments for lint, optimize, scan, and language or template arguments for generation.]

## Skill Version(s):

3.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
