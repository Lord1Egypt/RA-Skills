## Description:

一键搜索学术论文，自动下载PDF，智能总结核心工作与创新点。支持百度学术+arXiv，按引用量排序，科研必备工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiliuah](https://clawhub.ai/user/weiliuah)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this skill to search Baidu Scholar and arXiv, rank papers by citation or relevance signals, summarize core contributions and novelty, and download PDFs into organized local folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads remote PDF files to the user's Desktop papers folder.

Mitigation: Use it only when automatic PDF downloads are acceptable, and validate downloaded PDFs before opening files from unfamiliar sources.

Risk: The security evidence says the skill may contact Semantic Scholar or PDF hosts that are broader than the formal manifest clearly covers.

Mitigation: Review network permissions before deployment and run it only in environments where outbound access to academic sites and PDF hosts is permitted.

Risk: Installation guidance includes privileged package-manager commands for Poppler utilities.

Mitigation: Review system install commands before execution and install Poppler from trusted operating-system package sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weiliuah/skills/baidu-scholar-helper)
- [Baidu Scholar](https://xueshu.baidu.com)
- [arXiv API endpoint](https://export.arxiv.org/api/query)
- [Semantic Scholar](https://www.semanticscholar.org)
- [Google Scholar](https://scholar.google.com)
- [Citation feature documentation](docs/CITATION_FEATURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown search reports with inline command examples and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PDFs under ~/Desktop/papers/ and temporary extracted figure assets under /tmp/ when invoked.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
