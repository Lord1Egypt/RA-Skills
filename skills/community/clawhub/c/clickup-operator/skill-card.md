## Description: <br>
Route ClickUp ideas, to-dos, and project work with operator-style defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spotlight-revenue](https://clawhub.ai/user/spotlight-revenue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external ClickUp users use this skill to create, route, update, and read ClickUp ideas, to-dos, reminders, and project work with low-friction operating defaults. It helps an agent learn the user's workspace structure, apply configured assignment and due-date rules, and avoid unnecessary confirmation when the correct ClickUp action is clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live ClickUp changes, including creating, moving, assigning, or rescheduling work. <br>
Mitigation: Install it only when live ClickUp operation is intended, validate first with the safe-live smoke test or a test list, and give explicit requests for moves, assignments, rescheduling, and creation. <br>
Risk: Incorrect workspace, list, member, status, or due-date configuration can route work to the wrong place or person. <br>
Mitigation: Verify the configuration points to the intended workspace, lists, assignees, active statuses, and due-date defaults before normal use. <br>
Risk: ClickUp tokens or credentials could be exposed if users paste them into chat or logs during setup. <br>
Mitigation: Keep tokens out of chat and logs, and use the configured authentication path rather than sharing credentials in conversation. <br>


## Reference(s): <br>
- [ClickUp Operator ClawHub page](https://clawhub.ai/spotlight-revenue/clickup-operator) <br>
- [Routing Rules](references/routing-rules.md) <br>
- [Configuration](references/configuration.md) <br>
- [Guided Onboarding](references/guided-onboarding.md) <br>
- [Safe Live Validation](references/safe-live-validation.md) <br>
- [Structure Discovery](references/structure-discovery.md) <br>
- [Public Packaging](references/public-packaging.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, text] <br>
**Output Format:** [Markdown responses with configuration guidance and ClickUp operation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update ClickUp tasks, ideas, assignments, due dates, list routing decisions, and setup or validation checklists through the connected ClickUp tool surface.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
