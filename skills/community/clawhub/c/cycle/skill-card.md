## Description: <br>
Design custom workflow cycles for any domain. Create structured, repeatable processes that become persistent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to design repeatable multi-phase workflows for recurring tasks, including defining triggers, completion criteria, phase handoffs, validation points, and persistent preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cycle state can accidentally capture secrets, credentials, private account details, or instructions that should not influence future work. <br>
Mitigation: Review proposed state files before use and exclude sensitive or inappropriate information from persistent preferences, patterns, and constraints. <br>
Risk: A generated workflow cycle may encode misleading process guidance if it is used for publishing, approvals, or merges without review. <br>
Mitigation: Review each generated cycle and its validation checkpoints before relying on it for approval-sensitive or release-sensitive work. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance and workflow structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed cycle phases, validation checkpoints, handoff guidance, and optional persistent state structure.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
