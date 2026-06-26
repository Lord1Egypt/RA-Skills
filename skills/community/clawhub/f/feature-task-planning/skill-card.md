## Description: <br>
将技术方案拆解为可执行的开发任务清单，每个任务适配 TDD 流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cping6](https://clawhub.ai/user/cping6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after requirements and technical design are complete to turn a feature plan into vertically sliced, TDD-ready development tasks with dependencies, estimates, and acceptance-criteria coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read project context and write a planning markdown file into the repository. <br>
Mitigation: Review the generated path and content before committing or relying on the plan. <br>
Risk: A generated task plan can be incomplete or misaligned if the requirements, technical design, or project context are missing or stale. <br>
Mitigation: Confirm the required inputs are current and verify acceptance-criteria coverage before implementation starts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cping6/feature-task-planning) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Feature task planning template](artifact/assets/feature-task-planning-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Files] <br>
**Output Format:** [Markdown task planning document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a persistent feature task plan organized by vertical slices, including task dependencies, estimates, verification criteria, and AC coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
