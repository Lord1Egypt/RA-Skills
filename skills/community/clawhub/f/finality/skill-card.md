## Description: <br>
Finality is packaged as a blockchain finality helper, while the artifact implements a local note/log CLI for adding, listing, searching, removing, exporting, and configuring entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to run or evaluate a local CLI that manages timestamped entries in ~/.finality. Review the mismatch between the claimed blockchain finality purpose and the implemented local note/log behavior before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is presented as a blockchain finality analyzer, but the artifact implements a local note/log data manager. <br>
Mitigation: Treat outputs as local notes rather than protocol security analysis, and verify any blockchain finality claims against independent trusted sources. <br>
Risk: Entries are stored under ~/.finality and exports may be written to the current directory. <br>
Mitigation: Avoid entering secrets, private keys, or sensitive protocol data; review ~/.finality and finality-export files after running the CLI. <br>
Risk: The security verdict is suspicious according to ClawHub scan evidence. <br>
Mitigation: Review the shell script before installing or executing it, and run it in a controlled environment when testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/finality) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output and exported JSONL or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local data under FINALITY_DIR, defaulting to ~/.finality, and can export finality-export.json or finality-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
