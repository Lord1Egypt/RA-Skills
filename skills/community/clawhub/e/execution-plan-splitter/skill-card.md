## Description: <br>
Breaks large goals into 30/60/90-day execution paths, milestones, resource needs, abandonment criteria, and review-ready next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to convert goals, resource constraints, and time windows into structured execution plans for quarterly planning, transition projects, or new-role ramp-up. It is intended to produce reviewable drafts, checklists, and items needing confirmation before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python helper can inspect local files and surface sensitive-looking content if audit-oriented modes are enabled. <br>
Mitigation: Use the skill only with explicit planning documents, avoid whole repositories and sensitive directories, and review or remove audit-oriented modes before use in sensitive workspaces. <br>
Risk: Execution plans may contain assumptions or incomplete commitments when source inputs are sparse. <br>
Mitigation: Review the draft before execution, keep to-be-confirmed items visible, and require formal approval for budgets, external actions, publishing, or configuration changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/execution-plan-splitter) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON, with optional local shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 30/60/90-day sections, milestones, resource needs, abandonment criteria, items to confirm, and next-step guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
