## Description: <br>
A command-line skill advertised for attestation analysis that provides local entry management commands for status, add, list, search, remove, export, stats, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users can use this skill to run a small local CLI for storing, searching, listing, removing, exporting, and configuring attestation-labeled entries. Security evidence indicates it should be reviewed as a local data-storage utility rather than relied on as an attestation-analysis tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill is advertised as attestation analysis but behaves like a local note/data manager. <br>
Mitigation: Review the script behavior before use and do not rely on it for protocol security analysis without independent validation. <br>
Risk: The security guidance warns that entered data may be saved under ~/.attestation and exported to local files. <br>
Mitigation: Do not enter private keys, secrets, confidential protocol details, or sensitive identifiers unless local storage and export are acceptable. <br>


## Reference(s): <br>
- [ClawHub Attestation release](https://clawhub.ai/bytesagain1/attestation) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Terminal text output with optional JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local entries under ~/.attestation by default, or under ATTESTATION_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
