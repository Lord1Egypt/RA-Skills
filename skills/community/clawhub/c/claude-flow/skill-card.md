## Description: <br>
Claude Flow helps agents install, configure, and use a Claude Code multi-agent orchestration platform for coordinated software engineering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to set up Claude Flow or Ruflo in Claude Code, start specialist agents or swarms, and coordinate code implementation, review, security audit, testing, documentation, and troubleshooting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release suspicious because it grants broad install and automation authority with limited scoping guidance. <br>
Mitigation: Review the skill before installing it and enable MCP tools, hooks, memory, and automatic agent workflows only in projects where broad code-reading, code-writing, command execution, and local state changes are acceptable. <br>
Risk: Installation instructions include a curl-to-bash path that can execute remote code. <br>
Mitigation: Prefer npx or a pinned release, and inspect any installer script before running it. <br>
Risk: The skill requires API credentials and shows workflows involving environment variables and .env files. <br>
Mitigation: Protect API keys and .env files, avoid committing secrets, and provide credentials only in trusted local runtime configuration. <br>


## Reference(s): <br>
- [Claude Flow ClawHub page](https://clawhub.ai/cn-big-cabbage/claude-flow) <br>
- [Claude Flow homepage](https://github.com/ruvnet/claude-flow) <br>
- [Claude Flow npm package](https://www.npmjs.com/package/claude-flow) <br>
- [Installation guide](guides/01-installation.md) <br>
- [Quickstart guide](guides/02-quickstart.md) <br>
- [Advanced usage guide](guides/03-advanced-usage.md) <br>
- [Troubleshooting guide](troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to install packages, configure MCP servers, run local commands, and manage API-key-backed provider settings.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
