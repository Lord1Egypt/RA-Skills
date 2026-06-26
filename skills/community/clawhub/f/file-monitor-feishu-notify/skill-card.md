## Description: <br>
Monitors a configured local directory and sends Feishu group notifications when new files appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyoujin-cd](https://clawhub.ai/user/huyoujin-cd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to watch a single configured local folder and alert a Feishu group when new files are detected. It is suited to workflow automation where file arrival events should trigger lightweight team notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs background file monitoring and can send file names, sizes, timestamps, and local paths to a Feishu group. <br>
Mitigation: Configure it only for a narrow, non-sensitive folder and confirm the destination chat before enabling automatic notifications. <br>
Risk: Feishu app credentials are stored in config.json for API access. <br>
Mitigation: Use least-privilege Feishu credentials, restrict file permissions on config.json, and avoid committing real secrets. <br>
Risk: Automatic startup and process supervision may make the monitor persist beyond a user's immediate session. <br>
Mitigation: Verify the launcher or HEARTBEAT setup before use and document how to stop or disable the background process. <br>
Risk: The artifact documentation includes a GitHub push pattern with a token embedded in the remote URL. <br>
Mitigation: Do not use token-in-URL commands; use a credential manager, GitHub Desktop, or SSH-based authentication instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huyoujin-cd/file-monitor-feishu-notify) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with JSON configuration examples and PowerShell command snippets; runtime notifications are plain text sent to Feishu.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime messages can include file names, sizes, timestamps, and local paths from the configured watch directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
