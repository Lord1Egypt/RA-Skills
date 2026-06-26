## Description: <br>
An arXiv paper search engine for scientific researchers that supports broad and top-tier-filtered search, relevance and date sorting, duplicate checks, PDF downloads, and local CSV library management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tartykisser](https://clawhub.ai/user/tartykisser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and AI practitioners use this skill to search arXiv for AI papers, choose broad or top-tier-filtered retrieval, download selected PDFs, and maintain a local paper library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads external arXiv PDFs and writes them to the local workspace. <br>
Mitigation: Use an isolated Python environment and workspace, and review candidate papers before download when storage or privacy matters. <br>
Risk: The skill persists downloaded-paper history in paper_list.csv. <br>
Mitigation: Periodically inspect or clear paper_list.csv if retained download history is not desired. <br>
Risk: The skill depends on Python packages and network access to query arXiv and fetch PDFs. <br>
Mitigation: Install dependencies in an isolated environment and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tartykisser/ai-paper-researcher) <br>
- [arxiv-mcp upstream acknowledgement](https://github.com/Ractorrr/arxiv-mcp) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands, JSON tool output, downloaded PDF files, and CSV records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads selected arXiv PDFs and records downloaded paper metadata in a local CSV library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
