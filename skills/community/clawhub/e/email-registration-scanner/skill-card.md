## Description: <br>
Scans email accounts for registration, welcome, and confirmation messages, then returns a deduplicated chronological list of services the user signed up for. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatihbtw](https://clawhub.ai/user/fatihbtw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to scan selected email accounts and reconstruct a registration history for account cleanup, privacy review, or digital-footprint reduction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad mailbox access can expose sensitive email metadata and reveal account history. <br>
Mitigation: Scan only the smallest set of accounts needed and install only when temporary mailbox access is acceptable. <br>
Risk: IMAP scans may require temporary app passwords or provider bridge credentials. <br>
Mitigation: Prefer OAuth or provider-scoped app passwords, avoid regular account passwords, use a secret store where available, and revoke temporary app passwords after use. <br>
Risk: Plaintext IMAP weakens transport security if used beyond a local bridge. <br>
Mitigation: Use plaintext IMAP only for a local Proton Bridge connection and do not weaken provider security settings to make scans work. <br>
Risk: registration_scan JSON outputs can contain sensitive account-history data. <br>
Mitigation: Delete registration_scan JSON output files after reviewing results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fatihbtw/email-registration-scanner) <br>
- [Email Provider Reference](artifact/references/providers.md) <br>
- [Registration Search Queries](artifact/references/search-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown service list with inline shell commands; IMAP helper output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary registration_scan JSON files that contain mailbox-derived account history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
