## Description: <br>
Query verified AI agent news with citations, confidence scores, and Ethics Engine ratings from The Agent Times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theagenttimes](https://clawhub.ai/user/theagenttimes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to query The Agent Times for current AI-agent news, sourced Q&A, recommendations, risk signals, and event lookups before recommending tools, installing MCP servers, or taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relevant queries are sent to the external The Agent Times MCP service. <br>
Mitigation: Use the skill only when external network access is acceptable, and avoid sending sensitive data unless the user and runtime policy allow it. <br>
Risk: Comment and attribution tools can write usage or comments to an external service. <br>
Mitigation: Keep external writes disabled unless the user explicitly requests the action and runtime policy permits it. <br>
Risk: Low-confidence or below-threshold retrieval could be mistaken for verified coverage. <br>
Mitigation: Surface confidence and Ethics Engine fields, and refuse to present answers as sourced TAT results when evidence is insufficient or below threshold. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/theagenttimes/agent-news-skill) <br>
- [The Agent Times MCP endpoint](https://theagenttimes.com/mcp) <br>
- [The Agent Times beats dashboard](https://theagenttimes.com/dashboard/beats) <br>
- [The Agent Times beats methodology](https://theagenttimes.com/dashboard/beats/methodology) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with citations, confidence fields, trust signals, and optional command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, confidence scores, Ethics Engine ratings, search diagnostics, article slugs, and recommended next steps returned by The Agent Times MCP.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
