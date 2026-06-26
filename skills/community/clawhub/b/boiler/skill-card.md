## Description: <br>
Boiler is advertised as a boiler efficiency and sizing tool, but release security evidence says it behaves as a simple local record keeper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run a local CLI for recording, listing, searching, deleting, exporting, and summarizing entries under BOILER_DIR or ~/.boiler. Review security guidance before using it for real boiler sizing because release evidence says it behaves as a local record keeper rather than a boiler calculator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a boiler efficiency and sizing tool, but security evidence says it behaves as a local note keeper. <br>
Mitigation: Install only when that record-keeping behavior is intended; do not rely on it for boiler sizing or efficiency calculations without independent validation. <br>
Risk: Entries are stored locally in JSONL under BOILER_DIR or ~/.boiler and can contain arbitrary user-provided text. <br>
Mitigation: Do not store secrets, sensitive facility information, or regulated operational data in the local data directory. <br>
Risk: Remove and export commands directly mutate or copy local files with limited safeguards. <br>
Mitigation: Review command arguments before execution and back up any local data that must be preserved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/boiler) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with shell command examples; script output is plain text with JSONL or CSV data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSONL data under BOILER_DIR or ~/.boiler and may export boiler-export.json or boiler-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
