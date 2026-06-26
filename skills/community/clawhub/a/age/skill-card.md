## Description: <br>
Age is a file encryption reference covering key generation, X25519 encryption, SSH key support, passphrase mode, pipe patterns, SOPS integration, YubiKey plugins, and security considerations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and security practitioners use this skill as a quick reference for age encryption workflows, including key management, encrypting and decrypting files, backups, team sharing, SOPS, plugins, and security limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-pasted encryption examples may use the wrong recipient key or private identity file. <br>
Mitigation: Verify recipient keys before encrypting, protect private age and SSH identity files, and test decryption on non-sensitive sample data before relying on a workflow. <br>
Risk: Backup and cloud examples can affect real systems or data when adapted directly. <br>
Mitigation: Review cloud, database, and cleanup commands before execution, and preview destructive cleanup behavior before using deletion flags on real backups. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/age) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style reference text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact script prints reference material for selected age topics; it does not perform encryption operations itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
