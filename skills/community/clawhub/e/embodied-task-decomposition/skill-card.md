## Description: <br>
Decomposes complex physical tasks into atomic robot-executable subtasks from a scene image and natural-language task instruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanaoisong](https://clawhub.ai/user/nanaoisong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics practitioners use this skill to turn a physical scene image plus a task instruction into a sequential list of atomic robot actions with gripper choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated robot task steps may be incomplete, unsafe, or unsuitable for a real physical environment. <br>
Mitigation: Review every generated step before using it with a real robot and require manual approval for execution. <br>
Risk: New action-bank entries could introduce overly broad or unsafe future defaults. <br>
Mitigation: Manually review action-bank additions for duplicates, scope, and safety before accepting them. <br>


## Reference(s): <br>
- [Atomic Action Bank](references/action-bank.md) <br>
- [Task Decomposition Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown numbered list of robot subtasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each subtask uses an action-bank action and specifies left, right, or either gripper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
