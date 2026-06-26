## Description: <br>
Design Engineering guides agents through iterative frontend design work using research, planning, sub-agent execution, validation, and refinement loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design engineers use this skill to plan, implement, validate, and refine design-heavy frontend work that needs technical tradeoff analysis, sub-agent coordination, and visual QA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may edit project files, coordinate sub-agents, run local build or validation commands, and leave research notes in the project directory. <br>
Mitigation: Use it only in trusted project workspaces, keep normal command and file-change approvals enabled, review diffs, and run the validation checklist before accepting changes. <br>
Risk: Frontend changes produced through iterative design work can introduce layout, accessibility, responsiveness, or CSS-JS integration regressions. <br>
Mitigation: Run build checks, syntax checks, responsive spot checks, theme and reduced-motion checks, and screenshot review as described in the bundled validation checklist. <br>


## Reference(s): <br>
- [Design Engineering Skill Definition](artifact/SKILL.md) <br>
- [Rendering Technology Decisions](artifact/references/rendering-decisions.md) <br>
- [Sub-Agent Patterns for Design Work](artifact/references/subagent-patterns.md) <br>
- [Validation Checklist](artifact/references/validation-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/corbin-breton/design-engineering) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, command examples, implementation plans, and validation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Project-scoped workflow; no external credentials or services are required by the skill.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
