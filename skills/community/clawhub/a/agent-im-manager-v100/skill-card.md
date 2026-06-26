## Description: <br>
Multi-Agent conversation management platform with Gemini-style UI for managing OpenClaw agents with image upload, chat history, and message isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage local agents, create or delete agent records, and chat with selected agents through a browser UI, CLI, or local API. It is intended for trusted local operation where users review code and configure their own Operator Token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local service exposes unauthenticated controls that can run shell commands and create or delete local agent files. <br>
Mitigation: Run it only on a trusted local machine, keep port 3000 unavailable to other hosts, and prefer a version with authentication, agent ID and path validation, and removal of shell-string execution. <br>
Risk: The skill uses an Operator Token to connect to OpenClaw. <br>
Mitigation: Treat the token as a secret, avoid sharing config.json, and prefer a release that handles the Operator Token through a secret-management path. <br>
Risk: Browser-local chat history can retain sensitive chats or images. <br>
Mitigation: Avoid entering sensitive chats or images, clear browser storage when needed, and do not rely on private browsing for durable history. <br>
Risk: Agent creation and deletion can modify local OpenClaw agent directories. <br>
Mitigation: Back up ~/.openclaw before use and review requested create, delete, and chat actions before exposing the service to workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szzg007/agent-im-manager-v100) <br>
- [Publisher profile](https://clawhub.ai/user/szzg007) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [README](README.md) <br>
- [QUICKSTART](QUICKSTART.md) <br>
- [SECURITY](SECURITY.md) <br>
- [CLAWHUB](CLAWHUB.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, JavaScript application files, JSON configuration, shell commands, and local API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local web application on port 3000 and stores chat history in the browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
