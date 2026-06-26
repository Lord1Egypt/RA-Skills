## Description: <br>
Access passwords, secure notes, secrets and OTP codes from Dashlane vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnarco](https://clawhub.ai/user/gnarco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and external users use this skill to ask an agent for Dashlane CLI guidance for reading vault items, syncing or locking the vault, configuring persistence, and handling secret injection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault retrieval commands can expose passwords, secure notes, secrets, and OTP codes through console output, JSON, files, logs, or downstream processes. <br>
Mitigation: Prefer clipboard or direct consumers over console or JSON output, avoid logged sessions, and review commands before execution. <br>
Risk: Secret injection, backup, and master-password persistence can write secrets to disk or pass them to another process. <br>
Mitigation: Use exec, inject, backup, or persistence settings only when explicitly requested and validate destinations, environment variables, and logs first. <br>


## Reference(s): <br>
- [Dashlane CLI documentation](https://cli.dashlane.com) <br>
- [ClawHub Dashlane skill page](https://clawhub.ai/gnarco/dashlane) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read, copy, print, inject, or back up vault secrets; review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
