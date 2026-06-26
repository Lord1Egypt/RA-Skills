## Description: <br>
Bounded evidence-first research workflow for software agents that reduces uncertainty, localizes issues, validates outputs, or summarizes evidence without taking architecture ownership or editing production code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leslie-ller](https://clawhub.ai/user/Leslie-ller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and supervising agents use this skill to keep triage, bug localization, validation runs, and evidence summaries narrow and evidence-first before assigning an implementation or architecture task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research output may be mistaken for an implementation or architecture decision. <br>
Mitigation: Keep a human or supervising agent responsible for final decisions and use the skill's bounded next-step handoff. <br>
Risk: Validation work may require inspecting relevant project files or running commands in the active workspace. <br>
Mitigation: Limit access to the files and commands needed for the task and review command execution under the user's normal project controls. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured task-specific sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized by task class, such as triage, localization, validation, or summary.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
