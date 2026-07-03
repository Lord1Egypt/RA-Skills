## Description: <br>
Multi-department AI agent organization setup: hierarchy design, triple-channel communication, daily reporting, autonomous learning, and audit routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygq19901001](https://clawhub.ai/user/ygq19901001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of multi-agent systems use this skill to define agent rosters, communication routes, daily reports, learning schedules, audit checks, and repair delegation rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A monthly maintenance cron template can publish skills and create GitHub releases. <br>
Mitigation: Do not deploy that cron until repository credentials, branch protections, dry-run behavior, rollback steps, and explicit human approval are in place. <br>
Risk: Cron templates can run recurring agent actions across departments. <br>
Mitigation: Review schedules, models, alert destinations, output paths, and first-run behavior before enabling any recurring job. <br>
Risk: Agent governance guidance may affect communication, audit, and escalation behavior across a multi-agent system. <br>
Mitigation: Adapt the roster, communication routes, and audit checks to the local operating model and review generated changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/agent-org-manager) <br>
- [Communication Patterns](references/communication-patterns.md) <br>
- [Cron Templates](references/cron-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with roster examples, communication protocols, audit checklists, and JSON cron configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployable cron templates and operational file paths that should be reviewed and adapted before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter lists 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
