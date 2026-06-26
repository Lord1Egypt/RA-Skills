## Description: <br>
Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rubenfb23](https://clawhub.ai/user/rubenfb23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, developers, and technical readers use this skill to find recent ArXiv papers by topic, author, category, or paper ID, summarize abstracts, and maintain a local research log of discussed papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discussed papers and summaries may be retained in the local memory/RESEARCH_LOG.md file. <br>
Mitigation: Avoid sensitive or confidential research topics unless local retention is acceptable, and periodically review or delete the log. <br>
Risk: Search terms are sent to the public ArXiv API when the search script runs. <br>
Mitigation: Use non-confidential queries and review search terms before execution. <br>


## Reference(s): <br>
- [ArXiv API query endpoint](https://export.arxiv.org/api/query) <br>
- [ClawHub release page](https://clawhub.ai/rubenfb23/arxiv-watcher-vigo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown summaries with ArXiv links and local research-log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append discussed paper metadata and summaries to memory/RESEARCH_LOG.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-01-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
