## Description: <br>
Search, download, and summarize academic papers from arXiv for AI/ML researchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ractorrr](https://clawhub.ai/user/Ractorrr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, content creators, and technical practitioners use this skill to find arXiv papers, inspect paper metadata and abstracts, download PDFs, and maintain an optional reading list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional MongoDB tracking stores saved-paper metadata in a configured database. <br>
Mitigation: Use a dedicated low-privilege MongoDB database and connection string when enabling tracking. <br>
Risk: PDF downloads write files to a local directory selected by configuration or command arguments. <br>
Mitigation: Choose the download directory deliberately and review downloaded files before sharing or executing any downstream workflow. <br>
Risk: Dependencies are declared with lower bounds, which can reduce install reproducibility. <br>
Mitigation: Prefer a pinned and regularly updated dependency set for managed deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ractorrr/arxiv) <br>
- [arXiv API Documentation](https://arxiv.org/help/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files] <br>
**Output Format:** [Markdown or plain text with optional JSON output and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use optional MongoDB configuration for reading-list storage and an optional local PDF download directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
