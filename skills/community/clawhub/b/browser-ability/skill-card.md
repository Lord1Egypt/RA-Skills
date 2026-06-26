## Description: <br>
This skill helps an AI agent retrieve data from websites that require user sign-in through a JavaScript MCP browser helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[faisalive](https://clawhub.ai/user/faisalive) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent call browser-related MCP tools, hand off manual website sign-in to the user, and resume data retrieval after authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an AI agent and an external MCP server to a real browser session through a broad CDP handoff. <br>
Mitigation: Install only when the publisher and SERVER_URL MCP server are trusted, and require explicit user approval before CDP browsing or authenticated data access. <br>
Risk: Authenticated browser sessions can expose sensitive account, payment, password, MFA, or account-settings data. <br>
Mitigation: Use an isolated browser profile with no sensitive sessions and avoid banking, payments, password, MFA, and account-settings pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/faisalive/browser-ability) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sign-in URLs and signin_id values for human-in-the-loop authentication flows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
