## Description: <br>
Deploy Tool is a Bash command-line utility for recording, searching, summarizing, and exporting timestamped deployment-related notes in local flat files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep a local command-line log of deployment activities, checks, status notes, and related operational entries. It supports searching recent activity, viewing summary statistics, and exporting stored notes as JSON, CSV, or TXT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment notes may include sensitive operational details and remain searchable on local disk. <br>
Mitigation: Do not enter passwords, tokens, private keys, or sensitive deployment details; periodically review or remove stored files under ~/.local/share/deploy-tool/. <br>
Risk: The skill is a deployment-note logger, not a PHP deployment automation tool. <br>
Mitigation: Use it for local tracking, summaries, and exports only; rely on separate reviewed deployment tooling for operational changes. <br>
Risk: Exported JSON, CSV, or TXT files may contain deployment history that should not be broadly shared. <br>
Mitigation: Review exported files before sharing and delete exports that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/deploy-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/bytesagain3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text command output with local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local flat-file logs and optional JSON, CSV, or TXT exports under ~/.local/share/deploy-tool/.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
