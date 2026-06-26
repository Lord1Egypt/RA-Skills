## Description: <br>
Design Tool is a local Bash utility for recording, viewing, searching, summarizing, and exporting timestamped design notes in flat files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and design workflow users can use this skill to log design activity, inspect recent entries, search notes, view basic statistics, and export local records from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect a Penpot integration, but the artifact behaves as a local Bash logging utility. <br>
Mitigation: Confirm the desired capability before installation and use it only for local note logging, searching, summaries, and exports. <br>
Risk: Typed entries are persistently stored under ~/.local/share/design-tool and may be visible in later searches or exports. <br>
Mitigation: Avoid entering secrets, credentials, private project details, or sensitive design notes unless local persistent storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/design-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [CLI text output with local flat-file logs and JSON, CSV, or TXT exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent data under ~/.local/share/design-tool; no external services or API keys are required.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
