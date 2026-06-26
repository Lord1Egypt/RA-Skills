## Description: <br>
WebSocket-based cross-language communication service for Python and other languages, with support for text, JSON, dict, bytes, images, files, folders, client management, heartbeat tracking, and Aliyun OSS-backed file transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement WebSocket-based real-time messaging, client coordination, and optional Aliyun OSS-backed file transfer across Python and other language clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud storage credentials and transferred files may expose sensitive data if shared too broadly or handled with excessive permissions. <br>
Mitigation: Use dedicated least-privilege OSS credentials, avoid sending broad or sensitive folders, and restrict downloads to trusted senders and safe directories. <br>
Risk: A WebSocket server bound to a broad network interface can expose messaging or file-transfer behavior to untrusted networks. <br>
Mitigation: Bind the server to localhost or a trusted interface when possible and verify the external pywayne package source before installing. <br>


## Reference(s): <br>
- [Pywayne Cross Comm ClawHub page](https://clawhub.ai/wangyendt/cross-comm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable names for Aliyun OSS configuration and async Python usage examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
