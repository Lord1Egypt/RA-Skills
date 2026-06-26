## Description: <br>
DeepWiki Ask queries DeepWiki MCP for repository answers, documentation structure, and documentation contents when given an owner/repo target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to ask DeepWiki questions about a repository, inspect its documentation structure, or retrieve documentation contents for a specified topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names, requested topics, and questions are sent to DeepWiki. <br>
Mitigation: Avoid including secrets, private code excerpts, credentials, or confidential internal details unless that data flow is approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/autoxj/deepwiki-ask) <br>
- [Publisher profile](https://clawhub.ai/user/autoxj) <br>
- [DeepWiki MCP endpoint](https://mcp.deepwiki.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the helper script, summarized by the agent as Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports question, structure, and contents modes; timeout and retry behavior are configurable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
