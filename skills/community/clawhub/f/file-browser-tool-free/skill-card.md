## Description:

文件浏览器(免费版) helps agents browse directories, preview text files, search file names and contents, and perform basic local file-management operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill for lightweight local file browsing, text preview, simple search, and basic file organization tasks. It is best suited to scoped workspace file management rather than unrestricted system-wide operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad command-driven local file mutation, including deletion and cross-filesystem moves, without clear workspace limits.

Mitigation: Limit use to a specific workspace, avoid sensitive directories, and require explicit confirmation before move, delete, rename, or copy operations.

Risk: The skill text should not be treated as a complete safety boundary for shell-based file operations.

Mitigation: Rely on host agent sandboxing, permission controls, and pre-execution review for file-management commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/file-browser-tool-free)
- [Detailed Reference](artifact/references/detail.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code examples; runtime results are text or status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, move, copy, create, or delete local files when the host agent has permission; no API key is required.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
