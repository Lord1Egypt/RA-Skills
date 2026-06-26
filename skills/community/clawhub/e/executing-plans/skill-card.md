## Description: <br>
Use when you have a written implementation plan to execute in a separate session with review checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenleiyanquan](https://clawhub.ai/user/chenleiyanquan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to carry out a written implementation plan in small batches, with critical review, verification, and feedback checkpoints before continuing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or unclear implementation plans can lead an agent to make incorrect changes. <br>
Mitigation: Use the skill only with trusted plans, review the plan before execution, and stop for clarification when instructions are unclear or verification fails. <br>
Risk: Final behavior depends on a referenced finishing skill after the plan tasks are complete. <br>
Mitigation: Review the referenced finishing-a-development-branch skill separately before relying on the final development handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenleiyanquan/executing-plans) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status updates with concise verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation changes, verification output, and requests for clarification when blocked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
