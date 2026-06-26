## Description: <br>
Web scraping and browser automation using AgentQL - query any webpage with natural language to extract structured data, interact with elements, and automate browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhua2020](https://clawhub.ai/user/dhua2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scrape webpages, extract structured data, and automate browser interactions with natural-language AgentQL queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect browser automation to an existing browser session. <br>
Mitigation: Use a fresh, isolated browser profile unless the agent should intentionally access an existing logged-in session. <br>
Risk: Generated scripts may submit forms, post content, purchase items, delete data, or change account state. <br>
Mitigation: Review scripts before running them and require confirmation before actions that modify accounts or external systems. <br>
Risk: The skill requires AGENTQL_API_KEY. <br>
Mitigation: Keep AGENTQL_API_KEY out of source control, logs, and shared command output. <br>


## Reference(s): <br>
- [AgentQL Developer Portal](https://dev.agentql.com) <br>
- [ClawHub Agentql Release](https://clawhub.ai/dhua2020/agentql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AgentQL query snippets and Playwright automation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
