## Description: <br>
Enterprise-grade security for OpenClaw - blocks malicious skills, detects hallucinated packages, and prevents prompt injection attacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinewaveai](https://clawhub.ai/user/sinewaveai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, OpenClaw users, skill authors, and security teams use this skill to scan skills, prompts, packages, generated code, and agent actions before execution or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to run an external npm/npx scanner. <br>
Mitigation: Install only when comfortable running that package, and review the package source or registry entry before use. <br>
Risk: Auto-fix behavior can change project files. <br>
Mitigation: Review all generated fixes before committing or deploying them. <br>
Risk: MCP and git-hook integrations can run scanner behavior automatically. <br>
Mitigation: Inspect MCP and git-hook configuration after enabling integrations so the user knows what will run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinewaveai/clawproof-security) <br>
- [agent-security-scanner-mcp GitHub repository](https://github.com/sinewaveai/agent-security-scanner-mcp) <br>
- [agent-security-scanner-mcp npm package](https://www.npmjs.com/package/agent-security-scanner-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline shell commands and scanner result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of an external npm/npx scanner that may return security grades, allow/warn/block decisions, SARIF output, and auto-fix suggestions.] <br>

## Skill Version(s): <br>
3.10.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
