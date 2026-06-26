## Description: <br>
Amr provides a local command-line tracker for AMR-labeled tasks, entries, status checks, exports, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can ask an agent to use or explain the bundled CLI for AMR-labeled local notes and task records, including status summaries, entry management, search, export, and configuration. It should not be treated as live robot fleet status or control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as an AMR fleet manager, but the security evidence characterizes it as a local notes and task tracker. <br>
Mitigation: Use it only for AMR-labeled local records and do not rely on it for live robot fleet status, dispatch, or control. <br>
Risk: Operational notes may be stored under ~/.amr and exported as JSON or CSV into the current working directory. <br>
Mitigation: Avoid storing sensitive operational data unless local file storage and export behavior are acceptable; set AMR_DIR to an approved location when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/amr) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSONL data under the configured AMR data directory and export JSON or CSV files into the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
