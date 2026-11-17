## Description:

扫描本地电子书库，自动提取元数据、分类整理、联网搜索书籍简介，生成Obsidian笔记的完整工作流。支持EPUB/MOBI/AZW3/PDF格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatblue](https://clawhub.ai/user/fatblue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan local ebook folders, extract book metadata, enrich entries with book introductions, and generate Obsidian-ready Markdown notes and index files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search step can invoke a caller-supplied PowerShell script.

Mitigation: Review the search script before use and run it only when it is known and trusted.

Risk: A crafted index can make note generation write outside the intended output folder.

Mitigation: Use a dedicated empty output directory and avoid untrusted index files until path containment is fixed.

Risk: The generated JSON index records book titles and full local file paths.

Mitigation: Treat the index as sensitive and avoid sharing it outside trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fatblue/skills/book-library-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated workflow artifacts include JSON indexes and Markdown notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local library indexes, categorized note folders, an Obsidian index page, and progress output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
