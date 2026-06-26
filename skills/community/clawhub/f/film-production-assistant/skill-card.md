## Description: <br>
Pre-production assistant for filmmakers that generates script breakdowns, shot lists, call sheets, production schedules, and budget estimates from scene descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidapx13](https://clawhub.ai/user/davidapx13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External filmmakers, producers, assistant directors, and production teams use this skill to turn scene or project details into practical pre-production documents for planning a narrative film shoot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Word export uses an unsafe shell command pattern when implemented directly from the artifact guidance. <br>
Mitigation: Prefer text output unless export is explicitly requested; implement export with safe file-writing and non-shell argument handling. <br>
Risk: Call sheets and schedules can contain sensitive personnel, location, access, movement, and contact details. <br>
Mitigation: Minimize personal phone numbers, exact addresses, access instructions, and movement details, and share full versions only with authorized cast and crew. <br>


## Reference(s): <br>
- [Script Breakdown Structure Reference](artifact/references/script-breakdown-structure.md) <br>
- [Shot List Structure Reference](artifact/references/shot-list-structure.md) <br>
- [Call Sheet Structure Reference](artifact/references/call-sheet-structure.md) <br>
- [Production Schedule Structure Reference](artifact/references/production-schedule-structure.md) <br>
- [Film Budget Structure Reference](artifact/references/budget-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown production documents with optional Word document export when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce script breakdowns, shot lists, call sheets, production schedules, budget estimates, and optional .docx files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
