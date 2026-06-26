## Description: <br>
Feature Implementation guides an agent through TDD-driven feature work by reading planning documents, executing staged or change-request development, and validating work through tests and acceptance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cping6](https://clawhub.ai/user/cping6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to implement planned feature stages or change requests with a strict RED-GREEN-REFACTOR workflow. It is intended for codebases that already have requirements, technical design, and task-planning documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to change project files, update task documents, and produce completion reports. <br>
Mitigation: Invoke it with an explicit feature stage or change request, review proposed file changes before committing, and run the requested tests and acceptance checks. <br>
Risk: Incorrect or incomplete planning documents can lead the agent to implement the wrong behavior. <br>
Mitigation: Confirm the requirements, technical plan, task plan, and acceptance criteria are present and current before starting implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cping6/feature-implementation) <br>
- [Stage completion report template](artifact/assets/stage-completion-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, command, and file-change outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update task documents and generate stage completion reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
