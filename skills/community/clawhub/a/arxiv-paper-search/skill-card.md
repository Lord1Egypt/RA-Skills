## Description: <br>
Searches arXiv papers, retrieves recent AI papers and PDF links, and parses paper content for academic research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to search arXiv, find recent AI papers, retrieve PDF links, and parse paper content in an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the Xiaobenyang service as an intermediary for arXiv lookups. <br>
Mitigation: Install and use it only when that intermediary is acceptable for the user's research workflow. <br>
Risk: The XBY_APIKEY is treated as a secret and can be stored in a local .env file. <br>
Mitigation: Keep .env out of shared repositories and workspaces, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/arxiv-paper-search) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [Xiaobenyang API key service](https://xiaobenyang.com) <br>
- [arXiv](https://arxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown responses with structured JSON results from tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY and may return raw upstream paper search or parsing data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
