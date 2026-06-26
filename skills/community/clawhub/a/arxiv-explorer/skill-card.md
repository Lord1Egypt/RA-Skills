## Description: <br>
Search, download, and explore arXiv academic papers. Use when the user needs to find research papers, download PDFs, get recent publications in a field, or summarize academic content from arXiv. Supports searching by keywords, categories, authors, and downloading papers for offline reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunuowu](https://clawhub.ai/user/xunuowu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to search arXiv, retrieve recent papers by category, inspect paper metadata and summaries, and download selected PDFs for offline reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to arXiv over an HTTP API endpoint. <br>
Mitigation: Avoid confidential, sensitive, or proprietary search terms when using the search and recent-paper commands. <br>
Risk: The download command writes PDF files to the user-selected path. <br>
Mitigation: Choose an intended output path and review downloaded PDFs before opening or sharing them. <br>
Risk: The support QR code is an optional off-platform donation prompt. <br>
Mitigation: Treat donation links as separate from the skill's core search and download function. <br>


## Reference(s): <br>
- [arXiv API query endpoint](http://export.arxiv.org/api/query) <br>
- [arXiv PDF download endpoint](https://arxiv.org/pdf/{arxiv_id}.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [CLI text output, optional JSON, and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, authors, publication date, arXiv ID, PDF URL, and a truncated summary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
