## Description: <br>
Search arXiv by keyword, filter by submitted date range, fetch arXiv papers from an arXiv ID or URL, convert papers into Markdown and PDF files in the workspace, and maintain daily topic archives with summary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elio040208](https://clawhub.ai/user/elio040208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to search arXiv, retrieve papers, convert paper content into local Markdown/PDF artifacts, and create grounded summaries or recurring topic archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv over HTTPS to search and retrieve paper content. <br>
Mitigation: Run it only in environments where outbound access to arXiv is expected and acceptable. <br>
Risk: The skill creates local PDFs, Markdown, metadata, summaries, search results, and sync state. <br>
Mitigation: Use a dedicated output or root directory to keep generated artifacts separate from existing workspace files. <br>
Risk: Generated summaries may be incomplete when conversion falls back to abstract-only content. <br>
Mitigation: Treat summaries as review aids and verify important claims against the generated paper Markdown or PDF. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elio040208/arxiv-paper-reader) <br>
- [Search result handling](references/search-usage.md) <br>
- [Summary template](references/summary-format.md) <br>
- [Topic sync example](references/topics.example.json) <br>
- [arXiv](https://arxiv.org) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and summaries, with generated Markdown, PDF, JSON, and metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create search result files, paper artifacts, topic archives, run manifests, and summary files in the workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
