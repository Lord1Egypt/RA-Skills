## Description: <br>
Search and download research papers from arXiv.org - Research version for OpenClaw agents. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and OpenClaw agents use this skill to search arXiv by query or category, inspect paper metadata, and download selected paper PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and imports the Python `arxiv` dependency. <br>
Mitigation: Use a virtual environment to control and review the dependency before running the skill. <br>
Risk: Searches and downloads contact arXiv and save requested PDFs under `~/Downloads/arxiv` by default. <br>
Mitigation: Run the skill only when network access to arXiv and local PDF downloads are expected for the task. <br>


## Reference(s): <br>
- [arXiv](https://arxiv.org) <br>
- [ClawHub package page](https://clawhub.ai/nantes/arxiv-osiris) <br>
- [Publisher profile](https://clawhub.ai/user/nantes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown and plain text with command examples, Python snippets, paper metadata, PDF URLs, and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include titles, summaries, authors, publication dates, arXiv IDs, categories, and PDF URLs; downloads are saved under ~/Downloads/arxiv by default.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
