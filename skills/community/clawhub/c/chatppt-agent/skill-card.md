## Description: <br>
Uses the ChatPPT CLI to help an agent generate PowerPoint presentations from a topic or from Word, PDF, Markdown, and text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kahn520](https://clawhub.ai/user/kahn520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through ChatPPT CLI authentication, parameter collection, presentation generation, polling, and retrieval of download or editor links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents and login or configuration data may be processed by a third-party service. <br>
Mitigation: Use the skill only with approved data, avoid confidential or regulated documents unless third-party processing is authorized, and do not share credentials or config output. <br>
Risk: Local CLI authentication can persist after use. <br>
Mitigation: Use `chatppt auth logout` or remove the local ChatPPT config when the CLI should no longer remain authenticated. <br>
Risk: The skill can invoke a web-search option that may add cost. <br>
Mitigation: Require explicit user confirmation before enabling `--web-search`; otherwise pass `--web-search=false`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kahn520/chatppt-agent) <br>
- [ChatPPT OpenClaw](https://chat-ppt.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run ChatPPT CLI commands, collect required user inputs, poll for task status, and present generated file or editor links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
