## Description: <br>
Audit Claude Code configuration for security vulnerabilities, misconfigurations, and injection risks using AgentShield across settings, MCP servers, hooks, agents, and hardcoded secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit Claude Code project configuration before setup, onboarding, commits, or periodic security hygiene reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to run a third-party npm scanner. <br>
Mitigation: Install only if the package is acceptable for the environment; prefer npx or a pinned package version. <br>
Risk: Scanning the wrong path can expose or act on unintended Claude configuration files. <br>
Mitigation: Scan only the intended Claude configuration path. <br>
Risk: Automatic fixes or initialization can modify local configuration. <br>
Mitigation: Review proposed changes before using --fix or init. <br>
Risk: Optional deep analysis may send sensitive configuration context to an external model service. <br>
Mitigation: Avoid ANTHROPIC_API_KEY deep-analysis mode for sensitive configs unless external analysis is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djc00p/claude-code-security-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and security review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run AgentShield with optional JSON, Markdown, or HTML report formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
