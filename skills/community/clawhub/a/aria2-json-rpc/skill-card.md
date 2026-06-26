## Description: <br>
Interact with aria2 download manager via JSON-RPC 2.0. Manage downloads, query status, and control tasks through natural language commands. Use when working with aria2, download management, or torrent operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azzgo](https://clawhub.ai/user/azzgo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to let an agent manage an aria2 download manager through documented Python scripts, including adding downloads, checking status, pausing or resuming tasks, and configuring download options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent start, stop, remove, purge, and monitor downloads in an aria2 instance. <br>
Mitigation: Require explicit confirmation before remove, purge, pause-all, resume-all, or global option changes. <br>
Risk: RPC access can expose control of the download manager if the endpoint or secret is mishandled. <br>
Mitigation: Keep the RPC secret private and prefer localhost or HTTPS for remote RPC. <br>
Risk: URLs, torrent files, and metalink files may cause unwanted or unsafe downloads. <br>
Mitigation: Review URLs and torrent or metalink files before adding them to aria2. <br>


## Reference(s): <br>
- [Execution Guide for AI Agents](references/execution-guide.md) <br>
- [Aria2 RPC Methods Reference](references/aria2-methods.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Configuration Guide](CONFIG.md) <br>
- [Official aria2 Documentation](https://aria2.github.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-RPC result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a configured aria2 RPC endpoint and can start, pause, resume, remove, purge, inspect, or configure downloads.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release; artifact metadata version 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
