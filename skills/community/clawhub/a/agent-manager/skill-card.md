## Description: <br>
Multi-Agent conversation management platform with Gemini-style UI. Manage all your OpenClaw agents in one place with image upload, chat history, and message isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage multiple local agents, create or register agents, chat with them through a web UI or CLI, upload images, and preserve separate chat histories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package exposes powerful local controls through a local web service and CLI. <br>
Mitigation: Run only on a trusted local machine and avoid exposing port 3000 to a network. <br>
Risk: A token-like secret is included in the package. <br>
Mitigation: Remove and rotate any real OpenClaw token included in the files before use. <br>
Risk: Shell command execution, authentication, path validation, and deletion safeguards require review before sensitive use. <br>
Mitigation: Do not use the skill for sensitive agents until those safeguards are fixed and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szzg007/agent-manager) <br>
- [Publisher profile](https://clawhub.ai/user/szzg007) <br>
- [ClawHub homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JavaScript source files, JSON configuration, shell commands, web UI, CLI commands, and HTTP API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js service on port 3000 and interacts with a local OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
