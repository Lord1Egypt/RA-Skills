## Description: <br>
A local credential-management skill for adding, listing, retrieving, deleting, auditing, generating, and backing up API tokens, account passwords, SSH keys, and related secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local third-party service credentials, generate passwords, track credential reads, create encrypted backups, and inspect audit history from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores API keys, passwords, SSH keys, and similar secrets in ~/.openclaw/workspace/secrets.json and can reveal full values through local command output. <br>
Mitigation: Install only when local secret storage is acceptable, keep terminals and CI logs private, and avoid raw listing or retrieval in logged sessions. <br>
Risk: Autocapture handles credential-like text and could persist sensitive values if explicitly saved. <br>
Mitigation: Treat autocapture as opt-in only and require explicit user confirmation before saving detected credentials. <br>
Risk: The release evidence warns not to rely on the secure-delete wording for forensic erasure. <br>
Mitigation: Use deletion for application-level removal and apply separate device, filesystem, or backup-retention controls when forensic erasure is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/creds-vault) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/luis1213899) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with local command examples and JSON-backed credential data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reveal full secret values through get, raw listing, export, restore, or backup-related workflows; outputs should be handled as sensitive.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
