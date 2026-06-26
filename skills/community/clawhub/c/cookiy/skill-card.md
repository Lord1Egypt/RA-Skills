## Description: <br>
AI-powered user research through natural language that installs the Cookiy MCP server and orchestrates tool workflows for study creation, AI interviews, discussion guide editing, participant recruitment, report generation, and optional quantitative questionnaires. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yupeng-dev](https://clawhub.ai/user/yupeng-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, product teams, and agents use Cookiy to plan user research, create or edit discussion guides, run AI-moderated interviews, recruit participants, generate insight reports, and work with optional quantitative questionnaires through Cookiy MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or repair an external MCP server and modify local MCP client configuration. <br>
Mitigation: Use only when the publisher and cookiy-mcp package are trusted, and review MCP configuration changes before operational use. <br>
Risk: Paid actions, checkout links, cash credit, report access, and recruitment launch can create financial or operational commitments. <br>
Mitigation: Require explicit user confirmation before checkout, cash-credit purchase, report-link retrieval that requires payment, or recruitment launch. <br>
Risk: Uploaded screenshots, research materials, interviews, and report share links may expose confidential user-research content. <br>
Mitigation: Confirm that uploads and share links are intended, avoid confidential screenshots unless approved, and use only URLs returned by Cookiy tools. <br>


## Reference(s): <br>
- [Cookiy ClawHub Page](https://clawhub.ai/yupeng-dev/cookiy) <br>
- [Study Creation Workflow](references/study-creation.md) <br>
- [AI Interview Workflow](references/ai-interview.md) <br>
- [Discussion Guide Editing Workflow](references/guide-editing.md) <br>
- [Recruitment Workflow](references/recruitment.md) <br>
- [Report & Insights Workflow](references/report-insights.md) <br>
- [Cookiy MCP Tool Usage Contract](references/tool-contract.md) <br>
- [Cookiy MCP Endpoint](https://s-api.cookiy.ai/mcp) <br>
- [Cookiy OAuth Discovery](https://s-api.cookiy.ai/.well-known/oauth-authorization-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with inline shell commands and structured MCP workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth setup steps, checkout links returned by tools, report share links, and exact Cookiy identifiers.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
