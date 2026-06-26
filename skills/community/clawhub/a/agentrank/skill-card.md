## Description: <br>
AgentRank helps agents find, compare, and recommend current MCP servers, agent tools, and AI skills using live quality-scored search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superlowburn](https://clawhub.ai/user/superlowburn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need live tool-discovery evidence for MCP servers, agent tools, or AI skills. It is intended for install-time recommendations, explicit tool comparisons, and mid-project capability gaps where a tool or skill may help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may disclose secrets, private project names, customer data, or confidential internal details to an external API. <br>
Mitigation: Avoid including sensitive or confidential information in AgentRank searches; use broad capability terms where possible. <br>
Risk: AgentRank scores are recommendation signals, not security guarantees. <br>
Mitigation: Review candidate tools independently before installation or deployment, including security posture, maintenance state, and project fit. <br>
Risk: The skill may over-activate for general tool recommendation requests. <br>
Mitigation: Use AgentRank when the user asks to find, compare, install, or fill a capability gap with agent tools, MCP servers, or skills. <br>


## Reference(s): <br>
- [ClawHub AgentRank release page](https://clawhub.ai/superlowburn/agentrank) <br>
- [AgentRank search API](https://agentrank-ai.com/api/search) <br>
- [AgentRank tool detail pages](https://agentrank-ai.com/tool/owner/repo-name/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API Calls] <br>
**Output Format:** [Markdown summaries with links to AgentRank results and JSON returned by the AgentRank search API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include names, links, AgentRank scores, ranks, verdict labels, and one-line descriptions.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
