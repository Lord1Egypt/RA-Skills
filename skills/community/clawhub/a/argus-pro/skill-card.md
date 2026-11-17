## Description:

Argus Pro scans Python and JavaScript codebases with 40+ rules for security, bugs, performance, and code quality, then reports prioritized findings with fix suggestions, trend tracking, CI-ready JSON output, and custom rule support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Python and JavaScript repositories for likely security, reliability, performance, and maintainability issues before code review or CI release gates. It is intended for local repository analysis and produces both human-readable findings and machine-readable JSON for pipeline use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installation command can modify the system Python environment.

Mitigation: Install dependencies in a virtual environment or with a pinned dependency file instead of using `--break-system-packages`.

Risk: Local scan reports may contain repository paths and source snippets from sensitive code.

Mitigation: Scan only repositories whose local report files can safely contain paths and snippets, and handle generated Markdown and JSON reports as sensitive artifacts when appropriate.

Risk: The skill requires a license key for execution.

Mitigation: Provide the license key through the LICENSE_KEY environment variable and avoid committing license material to source control or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/argus-pro)
- [Publisher profile](https://clawhub.ai/user/occupythemilkyway)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Console output plus Markdown and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LICENSE_KEY environment variable; optional settings control source path, language selection, severity filtering, maximum displayed findings, JSON output, CI failure behavior, and ignored paths.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
