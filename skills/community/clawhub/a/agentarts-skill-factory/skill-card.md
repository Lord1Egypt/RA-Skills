## Description: <br>
Huawei Cloud AgentArts workflow packaging factory that generates a standard Skill directory with SKILL.md and invoke_agentarts.py from workflow gateway, path, version, and authentication parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plovjet](https://clawhub.ai/user/plovjet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to wrap deployed Huawei Cloud AgentArts workflows into reusable OfficeAce-compatible Skill directories without hand-writing the skill definition or invocation script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated invocation script can include default AgentArts API keys and handles sensitive credentials. <br>
Mitigation: Use a restricted AgentArts token, pass credentials through AGENTARTS_API_KEY, and remove default keys from generated files before sharing or committing them. <br>
Risk: The generated invoker includes an IP-direct fallback that disables TLS certificate verification. <br>
Mitigation: Disable or audit the IP-direct TLS-bypass fallback before production use. <br>
Risk: The generator writes a new skill directory based on user-provided parameters. <br>
Mitigation: Generate only into an empty intended output directory and review the generated files before deployment. <br>


## Reference(s): <br>
- [Publisher profile](https://clawhub.ai/user/plovjet) <br>
- [ClawHub skill page](https://clawhub.ai/plovjet/agentarts-skill-factory) <br>
- [Project homepage](https://github.com/plovjet/agentArts-to-officeAce) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration] <br>
**Output Format:** [Generated Skill directory containing Markdown and Python files, with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skills require AgentArts connection parameters and should prefer AGENTARTS_API_KEY for credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
