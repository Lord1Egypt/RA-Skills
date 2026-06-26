## Description: <br>
Access and manage Bitwarden passwords securely using the official bw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yorha59](https://clawhub.ai/user/yorha59) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve Bitwarden vault data through the official bw CLI, including passwords, usernames, full item JSON, search results, sync operations, and TOTP codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Bitwarden session token can expose vault access if persisted in shell startup files or captured in terminal, chat, or tool logs. <br>
Mitigation: Use temporary Bitwarden sessions, avoid saving BW_SESSION in shell startup files, unset it after use, and ask the agent to reveal only the specific secret needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Text, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Bitwarden bw CLI and an active BW_SESSION environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
