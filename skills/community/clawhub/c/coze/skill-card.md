## Description: <br>
Coze is an AI bot development assistant for building Coze bots, plugins, workflows, knowledge bases, and publishing integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bot builders use this skill for guidance on creating Coze bots, connecting plugins and APIs, configuring knowledge bases, orchestrating workflows, and selecting publishing channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example API authentication patterns may be adapted with real Coze tokens. <br>
Mitigation: Store real tokens in environment variables or a secrets manager and avoid pasting secrets into prompts, examples, logs, or shared skill content. <br>
Risk: Bot workflows, knowledge bases, HTTP nodes, and custom plugins may process sensitive or regulated data. <br>
Mitigation: Review Coze data residency, retention, approved data classes, knowledge-base uploads, and external endpoints before connecting production data. <br>
Risk: Publishing channels and API integrations can expose bot behavior beyond the development environment. <br>
Mitigation: Test boundary cases and permissions before release, and review each publishing channel before enabling production access. <br>


## Reference(s): <br>
- [ClawHub Coze skill page](https://clawhub.ai/zhangifonly/coze) <br>
- [Coze chat API endpoint used in the skill example](https://api.coze.cn/v3/chat) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python API examples and Coze platform configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
