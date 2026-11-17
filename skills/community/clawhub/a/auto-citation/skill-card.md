## Description:

自动为学术文章添加参考文献，解析 Markdown、LaTeX 和 Word 文档以提取主题、关键词和现有引用，调用 academic-search 检索相关论文，并在用户确认后输出或插入 BibTeX、GB/T 7714 或 APA 格式引用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vigorouspp](https://clawhub.ai/user/vigorouspp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, students, and technical writers use this skill to add academic citations to drafts, papers, blog posts, and reports. It helps parse the source document, propose paper-search queries, present candidate references for confirmation, and format or insert the selected citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install steps run an unpinned remote academic-search dependency.

Mitigation: Pin the academic-search revision and Python package versions, install in a virtual environment, and review dependency setup before running scripts.

Risk: Document-editing scripts can modify input files or nearby bibliography files.

Mitigation: Keep backups, prefer explicit --output paths, and review diffs before accepting generated citation changes.

Risk: Generated or recommended references may be irrelevant, duplicated, or formatted incorrectly.

Mitigation: Require user confirmation of candidate papers and review the final bibliography against the target citation style.

Risk: Generated LaTeX bibliography content may be unsafe if compiled with permissive shell execution.

Mitigation: Do not compile generated LaTeX with shell escape enabled unless the bibliography content has been reviewed.

## Reference(s):

- [Citation Style Reference](artifact/references/citation-styles.md)
- [Workflow Examples](artifact/references/workflow-examples.md)
- [academic-search dependency](https://github.com/ustc-ai4science/academic-search)
- [ClawHub skill page](https://clawhub.ai/vigorouspp/skills/auto-citation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON document analysis, BibTeX entries, GB/T 7714 or APA reference text, and updated Markdown, LaTeX, Word, or bibliography files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write user-provided document files; citation insertion should use explicit output paths and human review.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
