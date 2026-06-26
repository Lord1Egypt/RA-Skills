## Description: <br>
Access and search a structured open source knowledge base of book summaries optimized for AI agents via the MCP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danpalmieri](https://clawhub.ai/user/danpalmieri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users connect this skill to the Books for Agents MCP service to search, browse, retrieve, generate, and submit structured book summaries for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects the agent to the external booksforagents.com service, sending search queries and submitted content outside the local environment. <br>
Mitigation: Install only when that service is trusted for the intended workflow and avoid sending sensitive queries or unpublished content unless approved. <br>
Risk: The skill can publish generated summaries to a shared knowledge base without clear rollback guidance. <br>
Mitigation: Require user confirmation before using suggest_book or submit_book, and review generated summaries before publishing because submitted content may persist or be shared externally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danpalmieri/books-for-agents) <br>
- [Books for Agents MCP Endpoint](https://booksforagents.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with MCP tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include search results, structured summary sections, backlog entries, generation templates, and submitted book-summary content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
