## Description: <br>
Builds reviewable cross-team dependency maps, key paths, fragile nodes, escalation points, and risk chains from user-provided project materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and project coordinators use this skill to organize task lists, owning teams, and predecessor relationships into dependency lists, critical paths, fragile-node analysis, escalation conditions, and reviewable follow-up guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive project details or personal information in input files may be copied into generated reports. <br>
Mitigation: Review and redact sensitive material before use, and prefer stdout or --dry-run when handling sensitive inputs. <br>
Risk: Supplying the wrong output path could write a report to an unintended local file. <br>
Mitigation: Review input and output paths before running the helper script. <br>
Risk: Generated dependency maps may reflect incomplete or incorrect source material. <br>
Mitigation: Treat outputs as reviewable drafts and confirm missing task, ownership, and dependency details before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/dependency-map-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with optional Mermaid draft diagrams and optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local output file when an output path is supplied; supports dry-run/stdout usage for sensitive material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
