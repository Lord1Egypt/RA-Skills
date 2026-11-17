## Description:

Searches, downloads, and explores arXiv academic papers by keyword, category, author, or arXiv ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunuowu](https://clawhub.ai/user/xunuowu)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this skill to search arXiv, inspect recent papers by category, and download PDFs for offline reading or follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests use a non-HTTPS arXiv API endpoint, which may expose queries or responses to transport-security issues.

Mitigation: Use the skill on trusted networks or update the API endpoint to HTTPS before deployment.

Risk: Remote paper metadata is displayed in terminal output.

Mitigation: Treat paper metadata as untrusted remote text and sanitize or escape it before display in stricter environments.

Risk: PDF downloads write files to user-selected output paths.

Mitigation: Review output paths before download and restrict writes to intended working directories.

## Reference(s):

- [ClawHub arXiv Explorer Skill Page](https://clawhub.ai/xunuowu/skills/arxiv-explorer)
- [arXiv API Query Endpoint](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Plain text search results, optional JSON, and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, authors, publication date, arXiv ID, PDF URL, and a truncated summary; downloads write PDFs to the requested output path.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
