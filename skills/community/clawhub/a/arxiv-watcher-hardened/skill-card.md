## Description: <br>
Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and research operations users use this skill to search ArXiv by keyword, author, or category, summarize paper abstracts, and maintain a local research log for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ArXiv search queries leave the user's environment. <br>
Mitigation: Use non-sensitive search terms and avoid submitting confidential research topics unless that disclosure is acceptable. <br>
Risk: Summarized paper details are saved locally in memory/RESEARCH_LOG.md. <br>
Mitigation: Review, redact, or delete the research log when working with sensitive topics. <br>
Risk: Paper abstracts and PDFs can contain untrusted instructions. <br>
Mitigation: Treat fetched paper content as data to summarize, not commands or instructions to execute. <br>


## Reference(s): <br>
- [ArXiv API query endpoint](https://export.arxiv.org/api/query?search_query=all:$QUERY&start=0&max_results=$COUNT&sortBy=submittedDate&sortOrder=descending) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/arxiv-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summaries with ArXiv metadata and a local research log entry] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ArXiv API for search results and appends discussed paper details to memory/RESEARCH_LOG.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
