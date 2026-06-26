## Description: <br>
Diagram as contract for agreed-upon AI development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonlinear](https://clawhub.ai/user/nonlinear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to open a local Mermaid-backed contract diagram for a Markdown file, visualize agreed implementation state, and update phase badges and notes during AI development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server exposes broad local file access and automatic write behavior without enough safeguards. <br>
Mitigation: Review before installing, use only with non-sensitive Markdown files, stop the localhost server when done, and avoid exposing port 8080 beyond the local machine. <br>
Risk: The skill may modify Markdown files while claiming diagrams or updating phase badges. <br>
Mitigation: Use a controlled workspace or explicit target file, keep backups or version control available, and confirm changes before relying on updated diagrams. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nonlinear/contract-diagram) <br>
- [Contract Diagram skill source link](https://github.com/nonlinear/skills/tree/main/contract-diagram/SKILL.md) <br>
- [Marked Markdown parser](https://github.com/markedjs/marked) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Mermaid diagrams, localhost commands, and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a localhost viewer on port 8080 and may write updates to the selected Markdown file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
