## Description: <br>
Gasless provides shell commands for storing, listing, searching, removing, exporting, and configuring local plaintext entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a local plaintext entry manager for notes or configuration-like records. It should not be treated as a gasless blockchain analysis tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's label and description can lead users to expect gasless blockchain analysis, while the observed behavior is local note and configuration storage. <br>
Mitigation: Use it only as a local entry manager and do not rely on it for protocol analysis, security evaluation, or on-chain concepts. <br>
Risk: User-entered data is stored in plaintext under ~/.gasless and exports may be written to the current working directory. <br>
Mitigation: Do not enter secrets, wallet data, API keys, incident notes, or sensitive protocol information unless plaintext local storage and export files are acceptable. <br>


## Reference(s): <br>
- [Gasless ClawHub release](https://clawhub.ai/bytesagain3/gasless) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSONL, CSV, and configuration files under ~/.gasless or the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
