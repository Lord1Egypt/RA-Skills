## Description: <br>
Scans files, repos, and directories for leaked secrets, including API keys, tokens, passwords, connection strings, private keys, and credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nirwandogra](https://clawhub.ai/user/nirwandogra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit files, directories, or repositories for accidentally committed credentials before publishing, committing, or deploying code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan reports can contain sensitive file paths and masked credential previews. <br>
Mitigation: Keep generated reports private and avoid committing them or uploading them to shared CI artifacts. <br>
Risk: The skill inspects files in the path selected for scanning. <br>
Mitigation: Run it only against projects or folders you intend to inspect. <br>
Risk: Detected real credentials may remain usable after the scan. <br>
Mitigation: Rotate any real credentials the skill finds and remove them from code or history. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [ClawHub release page](https://clawhub.ai/nirwandogra/credential-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report or JSON scan report, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks detected secret previews, reports severity counts, includes remediation guidance, and exits with status codes for clean, high, or critical findings.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
