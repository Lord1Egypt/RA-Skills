## Description: <br>
Use when the user has a rough problem and reads papers to collect transferable modeling ideas, architectures, training flows, optimization objectives, agent pipelines, or data construction methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snake-fan](https://clawhub.ai/user/snake-fan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and research assistants use this skill to turn a rough research problem or Research Question Card into an auditable Method Candidate Library of transferable modeling ideas from papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally creates and updates multiple Markdown files in a workspace, so an incorrect workspace root or artifact path can place notes somewhere unintended. <br>
Mitigation: Confirm the workspace root and review generated file paths before allowing the workflow to write or update files. <br>
Risk: Candidate Methods are research inspiration and can be mistaken for a committed method design. <br>
Mitigation: Keep the workflow's confirmation gates and boundary language intact, and require human review before treating candidates as design decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snake-fan/skills/05-method-inspiration) <br>
- [Source repository path](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/05-method-inspiration) <br>
- [Publisher profile](https://clawhub.ai/user/snake-fan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and concise interactive guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a structured workspace of method-inspiration notes; asks for confirmation at source, Method Needs, and Candidate Method gates.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
