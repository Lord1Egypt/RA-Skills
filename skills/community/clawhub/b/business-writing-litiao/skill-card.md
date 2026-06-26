## Description: <br>
Business Writing Litiao helps agents draft sourced business reports, business insights, consulting analyses, company research, competitive analysis, user research, market analysis, and related business-writing outputs using Tavily-backed research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external business users, and analysts use this skill to produce sourced industry research reports, business insights, consulting analysis, company research, competitive analysis, user research, and market analysis in Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business research queries may be sent to Tavily when source gathering is used. <br>
Mitigation: Install only if Tavily use is acceptable for the intended data, and avoid sending confidential queries unless approved. <br>
Risk: The skill depends on a separate Tavily helper skill and a TAVILY_API_KEY. <br>
Mitigation: Review the Tavily helper skill before use and configure the API key through approved secret handling. <br>
Risk: Generated business reports can contain misleading claims if cited sources are not checked. <br>
Mitigation: Follow the skill's source verification and cross-reference instructions before relying on generated analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/business-writing-litiao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with citations, tables, and Mermaid diagrams when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY when Tavily-backed source gathering is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
