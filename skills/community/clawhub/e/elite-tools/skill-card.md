## Description:

Elite CLI tooling for efficient shell operations with optimized token usage across file discovery, file viewing, replacement, structural search, structured output, YAML processing, diffs, concise help, and HTML-to-Markdown conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bezkom](https://clawhub.ai/user/bezkom)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to choose efficient modern CLI tools for shell work, file traversal, file inspection, structured parsing, configuration edits, and command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to propose powerful shell commands for deletion, in-place rewrites, global configuration changes, or network fetches.

Mitigation: Review proposed commands before approval, especially outside version-controlled projects.

Risk: CLI recommendations can be incorrect for systems where the preferred tools are unavailable or use different binary names.

Mitigation: Confirm tool availability and platform-specific binary names before relying on generated commands.

## Reference(s):

- [Tool Examples](references/tool-examples.md)
- [Elite CLI Tools - Deep Dive](references/tools-deep-dive.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
