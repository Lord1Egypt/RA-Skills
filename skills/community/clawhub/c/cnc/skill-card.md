## Description: <br>
CNC machining program manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, machinists, or operations users can use this skill to keep lightweight local CNC-related notes or records through a shell-based tracker. It is for local record management, not G-code validation, CNC safety checking, or machine control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the CNC-labeled tracker for machine-control or G-code safety tooling. <br>
Mitigation: Use it only for local notes or records; do not rely on it for G-code validation, CNC safety checks, or machine control. <br>
Risk: The remove command edits local records, and export writes or overwrites cnc-export.json or cnc-export.csv in the current directory. <br>
Mitigation: Review local data before removal and check the current directory before exporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/cnc) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Configuration] <br>
**Output Format:** [Markdown command guidance, CLI stdout, JSONL local records, and optional JSON or CSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores records under ~/.cnc by default; CNC_DIR can override the data directory; export writes cnc-export.json or cnc-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
