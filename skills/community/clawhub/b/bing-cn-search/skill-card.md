## Description: <br>
Uses Bing CN search to retrieve current web information and summarize results with cited source sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvenSix66](https://clawhub.ai/user/EvenSix66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user asks for Chinese-language web search, recent news, current events, or online information that requires Bing CN results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and result retrieval are routed through Bing CN and may expose sensitive topics to an external search provider. <br>
Mitigation: Avoid using the skill for secrets, credentials, private personal information, or confidential work topics. <br>
Risk: Search results come from third-party websites and may be stale, incomplete, or inaccurate. <br>
Mitigation: Review the listed sources and verify important claims before relying on the summarized answer. <br>
Risk: The setup requires adding npm tools and an MCP server before use. <br>
Mitigation: Install only in environments where the listed tools are acceptable and confirm the configured MCP server before running searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EvenSix66/bing-cn-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with source list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are summarized in prose and followed by source website names and domains.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
