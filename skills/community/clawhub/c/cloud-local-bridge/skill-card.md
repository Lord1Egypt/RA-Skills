## Description: <br>
实现云端 OpenClaw 与本地 OpenClaw 之间的双向通信桥接。支持自然语言配对、命令执行、文件同步。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[84191879](https://clawhub.ai/user/84191879) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to pair cloud and local OpenClaw instances, route commands to a local machine, and move files between environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote users may gain broad control over local command execution and file access. <br>
Mitigation: Install only when remote control of this machine is intended, run the bridge as a low-privilege user, and require command and file allowlists plus confirmation on sensitive systems. <br>
Risk: Exposing the bridge directly to the internet could make local commands, files, and tokens reachable beyond the intended pairing. <br>
Mitigation: Bind the service to localhost or a private tunnel, protect and rotate the bearer token, and avoid direct public exposure. <br>


## Reference(s): <br>
- [Cloud-Local Bridge Examples](references/EXAMPLES.md) <br>
- [Cloud-Local Bridge on ClawHub](https://clawhub.ai/84191879/cloud-local-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands and configuration that enable remote command execution and file transfer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
