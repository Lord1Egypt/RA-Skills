## Description: <br>
Dropbox Business provides managed OAuth access for administering Dropbox Business teams, including members, groups, folders, devices, audit logs, sharing, file requests, and member file access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Dropbox Business administrators and operations teams use this skill to inspect and administer team resources through a Maton-managed OAuth connection. It supports guarded Dropbox Business API workflows where write, delete, and member file access actions require explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants a third-party gateway admin-level access to a Dropbox Business team. <br>
Mitigation: Install only when that access is intended, use the least-privileged admin account available, review Dropbox OAuth permissions, and keep MATON_API_KEY protected. <br>
Risk: Write, delete, and member-file-access actions can change team resources or expose sensitive member files. <br>
Mitigation: Require explicit user confirmation with specific resource identifiers and a business justification before those actions are executed. <br>
Risk: High-impact operations such as member removal, device revocation, admin-role changes, and permanent folder deletion may be difficult or impossible to reverse. <br>
Mitigation: Summarize consequences before execution, prefer reversible actions where available, and confirm destructive flags such as wipe_data and keep_account. <br>


## Reference(s): <br>
- [Dropbox Business on ClawHub](https://clawhub.ai/byungkyu/dropbox-business) <br>
- [Maton](https://maton.ai) <br>
- [Dropbox Business API Documentation](https://www.dropbox.com/developers/documentation/http/teams) <br>
- [Dropbox Team Administration Guide](https://developers.dropbox.com/dbx-team-administration-guide) <br>
- [Dropbox Team Files Guide](https://developers.dropbox.com/dbx-team-files-guide) <br>
- [Dropbox Authentication Types](https://www.dropbox.com/developers/reference/auth-types) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python request examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a Dropbox Business OAuth connection; high-impact actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
