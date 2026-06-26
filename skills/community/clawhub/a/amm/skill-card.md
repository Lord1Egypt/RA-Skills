## Description: <br>
Provides shell commands for an AMM-named local entry manager with status, add, list, search, remove, export, stats, and config operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators can use this skill as a local note and log manager for entries, exports, and simple configuration. Do not rely on it for AMM or blockchain security analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as AMM or blockchain analysis, but the security evidence says the artifacts implement a persistent local entry manager. <br>
Mitigation: Treat the skill as a local note/log manager only and do not use it for AMM mechanism analysis, protocol security evaluation, or on-chain decision support. <br>
Risk: Entries and exports may persist sensitive notes, protocol details, or trading information under AMM_DIR, ~/.amm, or local export files. <br>
Mitigation: Avoid storing private keys, secrets, confidential protocol notes, or trading information unless local persistence and export are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/amm) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command output with optional JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local entries under AMM_DIR or ~/.amm and can export local data to files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
