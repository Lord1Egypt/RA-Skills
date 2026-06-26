## Description: <br>
Secure ArXiv paper search and download tool with local caching, AI summarization, research logging, and no shell command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houssameddinemaatallah](https://clawhub.ai/user/houssameddinemaatallah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to search ArXiv, cache paper metadata and PDFs, summarize papers, and maintain structured research logs for later export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted paper IDs can write files outside the intended cache. <br>
Mitigation: Use only normal arXiv IDs from trusted input until paper-ID path handling is fixed. <br>
Risk: The skill stores downloaded PDFs, cached metadata, and persistent research logs locally. <br>
Mitigation: Install only in workspaces where local ArXiv caching and research-log retention are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houssameddinemaatallah/arxiv-research-secure) <br>
- [Publisher profile](https://clawhub.ai/user/houssameddinemaatallah) <br>
- [ArXiv API endpoint](https://export.arxiv.org/api/query) <br>
- [ArXiv PDF endpoint](https://arxiv.org/pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance] <br>
**Output Format:** [JSON command results, Markdown tables and logs, and local cached paper files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ArXiv caching and a persistent research log under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
