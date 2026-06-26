## Description: <br>
AI job search and hiring skill that lets agents search public jobs and talent, then use authenticated workflows to apply, interview, negotiate offers, post jobs, manage candidates, and handle hiring-related payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonypk](https://clawhub.ai/user/tonypk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers, employers, and their agents use Agenhire to search jobs or talent, manage applications and interviews, negotiate offers, and coordinate cross-border hiring workflows through public endpoints, MCP tools, CLI commands, or REST API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can take consequential hiring actions such as registration, applications, interviews, offer responses, employer messages, job postings, and negotiations without consistently clear approval boundaries. <br>
Mitigation: Require explicit human approval for those actions, keep audit checks enabled, and configure daily limits, allowlists, salary bounds, and expiration dates before using autonomous mode. <br>
Risk: Authenticated use requires an AgentHire API key that can authorize candidate or employer actions. <br>
Mitigation: Store the API key in a secure credential mechanism, avoid pasting it into chat history, and rotate it if exposure is suspected. <br>
Risk: The skill includes crypto deposit or payment-related workflows. <br>
Mitigation: Require explicit approval for every deposit or payment step and verify recipient, amount, chain, and business purpose before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tonypk/agenhire) <br>
- [AgentHire Website](https://agenhire.com) <br>
- [AgentHire OpenAPI Spec](https://agenhire.com/api/docs/openapi.json) <br>
- [AgentHire Agent Protocol](https://agenhire.com/.well-known/agent.json) <br>
- [AgentHire AI Documentation](https://agenhire.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with JSON, HTTP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP server configuration, CLI commands, REST API requests, and approval guidance for high-impact actions.] <br>

## Skill Version(s): <br>
4.0.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
