## Description: <br>
Multi-Agent conversation management platform with Gemini-style UI. Manage all your OpenClaw agents in one place with image upload, chat history, and message isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add, manage, delete, pair, and chat with multiple local OpenClaw agents through a web UI, CLI, and local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated local controls can manage agents and conversations if port 3000 is exposed. <br>
Mitigation: Use only on a trusted local machine, keep the service bound to local access, and do not expose port 3000 until authentication and CORS are fixed. <br>
Risk: Shell command execution and token/configuration access can affect the local OpenClaw environment. <br>
Mitigation: Review the code before installing, rotate any token matching the examples, and avoid sensitive conversations until command execution and path validation are fixed. <br>
Risk: Delete and management operations can remove or alter local agent data. <br>
Mitigation: Back up important OpenClaw agent data and add delete safeguards before using the skill with important agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szzg007/agent-manager-v1) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [README](README.md) <br>
- [Quickstart](QUICKSTART.md) <br>
- [ClawHub release notes](CLAWHUB.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Web UI responses, JSON API responses, CLI text, and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js service on port 3000 and may read or write OpenClaw agent configuration and workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
