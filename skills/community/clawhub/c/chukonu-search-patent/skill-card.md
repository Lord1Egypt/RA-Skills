## Description: <br>
Searches China (CNIPA) and Europe (EPO) patent databases through the Chukonu remote MCP server with fielded Boolean search, record retrieval, OAuth login, read-only access, and enforced pagination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenybw](https://clawhub.ai/user/stevenybw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, patent analysts, and IP researchers use this skill to search CNIPA and EPO patent records, filter by structured patent fields, retrieve bibliographic data and claims, and check service quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote MCP server requires OAuth and stores access through the host environment. <br>
Mitigation: Install only when this patent-search access is intended, use the least-privilege account available, and re-run OAuth login only when authorization has expired. <br>
Risk: Patent searches and claims retrieval are quota controlled and paginated. <br>
Mitigation: Check usage before long runs, respect returned cursors, and stop or narrow searches when quota is near exhaustion. <br>


## Reference(s): <br>
- [Chukonu MCP server](https://search.houdutech.cn/mcp/) <br>
- [ClawHub skill page](https://clawhub.ai/stevenybw/chukonu-search-patent) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and MCP tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only remote MCP queries; OAuth login required; paginated search and claims retrieval; quota can be checked with usage().] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
