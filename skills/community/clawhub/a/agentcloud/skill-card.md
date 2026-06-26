## Description: <br>
AgentCloud helps AI agents register cloud storage, upload and download files, create share links, and check usage through REST API, CLI, and dashboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzh0202](https://clawhub.ai/user/jiangzh0202) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to give agents a managed file-storage workflow for registration, uploads, downloads, listing, sharing, and storage-plan checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files and API keys are handled by AgentCloud/traceclaw.cn. <br>
Mitigation: Use the skill only when you trust that service with the uploaded files and store API keys as secrets. <br>
Risk: Share URLs can expose files to anyone who has the link until they expire. <br>
Mitigation: Treat share URLs like secrets, use short expirations, and avoid sharing sensitive or regulated data unless the service controls meet your requirements. <br>
Risk: The download helper can write downloads to server-chosen local paths. <br>
Mitigation: Use explicit output paths, review downloaded filenames before relying on them, and be cautious with the helper until filename sanitization is fixed. <br>


## Reference(s): <br>
- [AgentCloud ClawHub listing](https://clawhub.ai/jiangzh0202/agentcloud) <br>
- [AgentCloud website](https://agentcloud.traceclaw.cn) <br>
- [AgentCloud API health endpoint](https://api.traceclaw.cn/health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands, Python examples, and CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local configuration containing an AgentCloud API key and may call the AgentCloud API when helper commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
