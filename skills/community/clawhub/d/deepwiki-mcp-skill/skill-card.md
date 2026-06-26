## Description: <br>
Ask questions and read documentation about GitHub repositories using DeepWiki MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to query indexed GitHub repositories, understand codebase structure, find APIs, and gather code review context through DeepWiki MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names and natural-language questions are sent to the external DeepWiki MCP service. <br>
Mitigation: Use the skill only for repositories and questions that are approved for sharing with DeepWiki; avoid secrets, access tokens, proprietary private-code details, and sensitive internal context. <br>
Risk: The skill depends on uxc, a local deepwiki-mcp-cli link, network access to mcp.deepwiki.com/mcp, and prior DeepWiki indexing. <br>
Mitigation: Confirm uxc is installed, review installation scripts before running them, verify the fixed command link, and index the target repository on DeepWiki before relying on results. <br>


## Reference(s): <br>
- [DeepWiki Usage Patterns](references/usage-patterns.md) <br>
- [DeepWiki](https://deepwiki.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and MCP JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are read from MCP JSON envelopes under .data.content[].text; DeepWiki supports up to 10 repositories per question.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
