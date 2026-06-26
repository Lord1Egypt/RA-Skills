## Description: <br>
Consensus provides shell commands for managing a local note-style entry store under ~/.consensus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users can use this skill to add, list, search, remove, export, and summarize local entries through shell commands. It should not be relied on as a blockchain consensus or protocol-security analyzer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as a blockchain consensus and protocol-security analyzer, while server security evidence says the artifacts implement a local persistent entry manager. <br>
Mitigation: Use it only for local entry management; do not rely on it for consensus analysis or protocol-security decisions. <br>
Risk: Remove and export commands can delete stored entries or create files in the current working directory. <br>
Mitigation: Review command arguments, back up ~/.consensus/data.jsonl, and run export from a controlled directory. <br>
Risk: Local entries may contain sensitive material because they are stored persistently under ~/.consensus. <br>
Mitigation: Avoid storing secrets or regulated data, and manage local file permissions and retention before sharing the machine or exports. <br>


## Reference(s): <br>
- [ClawHub Consensus release](https://clawhub.ai/ckchzh/consensus) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Plain text CLI output with JSONL or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ${CONSENSUS_DIR:-~/.consensus}; export creates consensus-export.json or consensus-export.csv in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
