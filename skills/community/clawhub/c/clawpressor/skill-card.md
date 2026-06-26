## Description: <br>
Session Context Compressor compresses OpenClaw session context with Sumy LexRank summarization to reduce token usage while preserving recent messages and creating backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beboxos](https://clawhub.ai/user/beboxos) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preview, apply, and restore session context compression when large session files slow work, approach context limits, or increase token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying compression modifies OpenClaw session files and could lose detail from older messages. <br>
Mitigation: Run the documented dry run first, keep the automatically created backup, and use restore if the compressed session is not acceptable. <br>
Risk: The security summary flags an under-disclosed Google Sheets path that can use local Google credentials and send compression activity metadata externally. <br>
Mitigation: Do not create the Google Sheets ID file or provide Google credentials unless external reporting is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/beboxos/clawpressor) <br>
- [README.md](README.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal output and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write compressed JSONL session files, backup files, local compression statistics, and optional Google Sheets compression activity rows when explicitly configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, config.yaml, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
