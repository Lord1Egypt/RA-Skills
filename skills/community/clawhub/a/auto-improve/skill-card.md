## Description: <br>
Helps an agent improve its future work by learning from mistakes, recognizing reusable patterns, and updating project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mcben90](https://clawhub.ai/user/Mcben90) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to make an agent check prior mistakes, reuse successful patterns, verify work, and record lessons after successful or failed actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to automatically store and reuse project learnings across sessions without clear consent, limits, or review controls. <br>
Mitigation: Require confirmation before writing learnings or reusing stored context, and review `.antigravity.md` changes before accepting them. <br>
Risk: Persistent project memory can capture sensitive repository context or secrets if used in sensitive workspaces. <br>
Mitigation: Avoid using the skill in sensitive repositories unless secret capture can be prevented and memory writes are restricted to reviewed, relevant content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Mcben90/auto-improve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown with checklists, pseudo-code, YAML trigger examples, and process tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or request persistent project-context and memory updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
