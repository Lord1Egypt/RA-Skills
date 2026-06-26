## Description: <br>
Search, download, and summarize academic papers from arXiv for AI and machine learning research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carloscbrls](https://clawhub.ai/user/carloscbrls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, technical writers, and security practitioners use this skill to search arXiv, inspect paper metadata, download PDFs, summarize papers, and maintain an optional reading list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download arXiv PDFs to local storage. <br>
Mitigation: Use explicit download requests and set ARXIV_PAPERS_DIR to a suitable directory when local storage location matters. <br>
Risk: Optional MongoDB persistence can store paper metadata and reading status. <br>
Mitigation: Leave MONGODB_URI unset unless that persistence is intended and the database is appropriate for the saved research metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/carloscbrls/cc3po-arxiv) <br>
- [ClawHub metadata homepage](https://clawhub.ai/carloscbrls/arxiv) <br>
- [arXiv API documentation](https://arxiv.org/help/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown responses with paper metadata, summaries, links, and optional local PDF downloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally use MongoDB for saved-paper metadata and ARXIV_PAPERS_DIR for local PDF storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
