## Description:

Helps agents find, download, configure, and develop packages for the Cangjie language ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l3gi0nxxxx](https://clawhub.ai/user/l3gi0nxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover Cangjie packages, download selected package artifacts, configure Cangjie project dependencies, and follow package development or publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose broad local changes, including project mutations, builds, package downloads, and TOML writes.

Mitigation: Review each proposed command and file edit before execution, especially commands that alter project configuration or download package artifacts.

Risk: The skill may suggest editing shell startup files or sourcing SDK setup scripts.

Mitigation: Require explicit user confirmation for shell profile changes and verify all paths are quoted and point to the intended Cangjie SDK location.

## Reference(s):

- [ClawHub cjpkg Release Page](https://clawhub.ai/l3gi0nxxxx/skills/cjpkg)
- [Cangjie Central Repository](https://pkg.cangjie-lang.cn/index)
- [Cangjie SDK Download](https://cangjie-lang.cn/download)
- [Cangjie Native Development Guide](https://gitcode.com/Cangjie/cangjie_docs/blob/main/docs/dev-guide/summary_cjnative_EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local project edits, package downloads, builds, and TOML dependency updates for user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
