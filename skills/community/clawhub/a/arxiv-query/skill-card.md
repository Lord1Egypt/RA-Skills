## Description: <br>
Search and summarize papers from ArXiv when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research-focused teams use this skill to search ArXiv by keyword, author, or category, summarize paper abstracts, and keep a local research log of discussed papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to ArXiv, which may expose sensitive or confidential research interests. <br>
Mitigation: Use non-confidential queries unless the user is comfortable sending the terms to ArXiv. <br>
Risk: Discussed paper details are saved locally in memory/RESEARCH_LOG.md. <br>
Mitigation: Review, redact, or delete the research log before sharing the workspace or using the skill with confidential research. <br>


## Reference(s): <br>
- [ArXiv API query endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown summaries with shell command usage and local research-log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query the ArXiv API and append summarized paper details to memory/RESEARCH_LOG.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
