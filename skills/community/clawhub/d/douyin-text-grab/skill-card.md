## Description:

从抖音链接提取视频或图文笔记的完整文案，并生成保留原文结构的 Word 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[csak47mu](https://clawhub.ai/user/csak47mu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a user provides a Douyin short link or share text and asks to extract the original copy into a Word document without summarization or rewriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Douyin titles, author names, or full post text may be placed into shell command arguments.

Mitigation: Pass scraped values through non-shell argument arrays, stdin, or temporary files rather than interpolating them into quoted command strings.

Risk: The skill accesses Douyin links and creates or sends DOCX files.

Mitigation: Review before installing and use only in environments where external Douyin access and DOCX file creation are expected.

## Reference(s):

- [ClawHub skill page for douyin-text-grab](https://clawhub.ai/csak47mu/skills/douyin-text-grab)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and DOCX file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates DOCX files from extracted Douyin text; requires python-docx for the helper script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
