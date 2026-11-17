## Description:

asclaude-grep helps agents search local OpenClaw workspaces by content or filename using grep-style regular expressions and filename patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaoxingjun](https://clawhub.ai/user/miaoxingjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate matching code, documents, configuration files, and filenames inside a local OpenClaw workspace during review, debugging, and refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search patterns that begin with command-style options can affect grep argument handling.

Mitigation: Avoid untrusted option-like patterns and prefer a patched version that inserts a grep -- delimiter or provides fixed-string search mode.

Risk: Search results can expose filenames or content from the local OpenClaw workspace.

Mitigation: Install and run the skill only in workspaces where local filename and content search is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miaoxingjun/skills/asclaude-grep)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with file paths, line numbers, and concise command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited to the first 20 matches and are generated from local workspace files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
