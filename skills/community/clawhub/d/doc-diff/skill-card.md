## Description:

Compare two documents or files and generate a structured diff report. Use when: user asks to compare files, find differences between documents, generate diff report, or check what changed between two versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content reviewers, and other external users use this skill to compare two files or directories and receive a structured summary of additions, deletions, and important changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects user-selected files or directories, which may expose sensitive content to the agent running the comparison.

Mitigation: Use the skill only with files and directories the user intends the agent to read, and avoid comparing sensitive material unless the environment is approved for that data.

Risk: The workflow relies on diff shell commands using user-provided paths.

Mitigation: Pass file paths safely as arguments, quote paths when needed, and avoid concatenating raw user input into shell commands.

Risk: The report is specified in Chinese, which may be unsuitable for users expecting another language.

Mitigation: Tell users that the default report language is Chinese and translate or regenerate the summary in another language when requested.

## Reference(s):

- [Document Diff skill source](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/cnoder-wgh/skills/doc-diff)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style structured report in Chinese with diff output and summarized changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the diff command-line tool; may read file contents or extracted text from binary documents selected by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
