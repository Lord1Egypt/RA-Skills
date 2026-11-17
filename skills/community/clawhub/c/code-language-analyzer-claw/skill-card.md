## Description:

Scans a project directory, detects programming languages, counts files and code lines by language, and produces a readable distribution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmgood](https://clawhub.ai/user/zmgood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand a project's language mix, code volume, and technology stack composition. It is useful for project audits, repository summaries, and language distribution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis script reads source files in the target directory, which may include private or sensitive project code.

Mitigation: Run it only on directories intended for local scanning and avoid sharing generated reports when repository contents are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmgood/skills/code-language-analyzer-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, plus plain text or JSON analysis reports from the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include file counts, total lines, non-empty code lines, percentages, and optional per-file detail.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
