## Description: <br>
Email Backup archives selected local directories as tar.gz files and can send them through QQ Mail SMTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dragonHuge](https://clawhub.ai/user/dragonHuge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to package selected folders, optionally clean common sensitive patterns, and send the resulting backup archive by QQ Mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can archive broad local paths and send them by email, which may expose private files or credentials. <br>
Mitigation: Use --no-send first, inspect archive contents, verify the recipient address, and avoid broad paths such as home directories, credential stores, SSH keys, browser profiles, and workspaces containing secrets. <br>
Risk: Sensitive-data cleaning is described as unreliable in the security guidance. <br>
Mitigation: Do not rely on --clean for secret removal unless the cleanup behavior is fixed and tested; rotate the QQ SMTP authorization code if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dragonHuge/email-backup) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime output includes tar.gz backup archives and SMTP email sends.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and QQ_EMAIL / QQ_SMTP_PASSWORD configuration for SMTP sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
