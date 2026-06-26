## Description: <br>
Fload helps agents use Fload MCP tools for mobile app analytics, reviews, growth metrics, ad performance, anomalies, and app store optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hassanbazzi](https://clawhub.ai/user/hassanbazzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mobile app publishers and growth teams use this skill to query Fload MCP tools for portfolio health, reviews, revenue and download metrics, ad performance, anomalies, forecasts, and growth audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent access sensitive Fload organization and app-business data. <br>
Mitigation: Install it only for intended Fload organizations, protect the FLOAD_API_KEY, and use the narrowest available Fload permissions or scopes. <br>
Risk: Review-reply approval tools can change or delete customer-facing review responses. <br>
Mitigation: Require explicit user confirmation before approving, editing, rejecting, sending, or deleting review replies. <br>
Risk: The documented MCP setup runs the @fload-ai/mcp package through npx. <br>
Mitigation: Verify the package source and version before running it in an agent environment. <br>


## Reference(s): <br>
- [Fload app](https://app.fload.app) <br>
- [ClawHub skill page](https://clawhub.ai/hassanbazzi/fload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline tool names, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide MCP API calls that retrieve sensitive app analytics and review-management data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
