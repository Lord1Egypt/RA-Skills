## Description:

Automated documentation generator for API docs, README files, changelogs, contributing guides, architecture docs, tutorials, FAQs, and reference manuals for REST and GraphQL projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate starter documentation for software projects, including API references, READMEs, changelogs, contribution guides, architecture descriptions, tutorials, FAQs, and reference manuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled local utility can persistently store and log user-provided text.

Mitigation: Do not pass secrets, credentials, proprietary content, or confidential text to script.sh; review its local data directory before sharing logs or artifacts.

Risk: Generated documentation includes hardcoded BytesAgain attribution.

Mitigation: Review generated documents before committing or publishing them and remove or adjust attribution where project policy requires.

Risk: The release security verdict is suspicious.

Mitigation: Review the skill before installation and run it in a controlled workspace until the bundled utility behavior is accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/docs-generator)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain feedback](https://bytesagain.com/feedback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text emitted by shell commands, with example code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents include hardcoded BytesAgain attribution in the bundled templates.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
