## Description: <br>
Helps an agent guide users through uploading files to a local OpenClaw workspace through a browser-based service for AI analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengwang86](https://clawhub.ai/user/chengwang86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to provide a local web upload page, manage uploaded files, and make local workspace files available for AI analysis without using cloud storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a persistent HTTP upload service on port 15170. <br>
Mitigation: Bind the service to localhost or protect it with firewall rules, and expose it only in environments where local file upload is intended. <br>
Risk: Authentication may be weakly scoped or absent depending on the user's OpenClaw configuration. <br>
Mitigation: Verify authentication against the actual OpenClaw configuration and avoid placing long-lived gateway tokens or passwords in shared browser URLs. <br>
Risk: The service can manage uploaded files and expose installed skill information. <br>
Mitigation: Install only in workspaces where file management and skill export endpoints are acceptable, and review access controls before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chengwang86/file-upload-to-local-workspace) <br>
- [Security audit](SECURITY-AUDIT.md) <br>
- [Authentication compatibility](docs/AUTH-COMPATIBILITY.md) <br>
- [AI reply guide](docs/AI-REPLY-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with URLs, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should avoid exposing real gateway tokens, passwords, or server IP addresses.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
