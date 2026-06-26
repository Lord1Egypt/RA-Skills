## Description: <br>
Multi-Agent conversation management platform with Gemini-style UI. Manage all your OpenClaw agents in one place with image upload, chat history, and message isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage local agents, create and delete agent records, and chat with agents from a browser UI, CLI, or local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful local agent controls through shell-backed web APIs. <br>
Mitigation: Run it only on a trusted local machine, keep the service off untrusted networks, and replace shell-built commands with argument-based process calls or native APIs before broader use. <br>
Risk: Operator Tokens or other OpenClaw credentials may be placed in plaintext configuration. <br>
Mitigation: Avoid real Operator Tokens in plaintext config and use a secret store or environment-based configuration where possible. <br>
Risk: Create, chat, and delete operations can affect local OpenClaw agent state. <br>
Mitigation: Back up ~/.openclaw before installation and add authentication or access controls before exposing these operations outside a trusted browser session. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/szzg007/agent-manager-v100) <br>
- [Project homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text and Markdown chat responses, JSON API responses, shell command examples, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against the user's OpenClaw workspace and browser-stored chat history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
