## Description:

Creates domain-expert agent skills with self-learning, review, trend-scanning, planning, and continuous evolution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyao721](https://clawhub.ai/user/wuyao721)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design, create, review, and upgrade self-evolving domain-expert skills. It also guides learning plans, trend scans, permissions templates, reports, and logs for skill ecosystems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and evolve other skills, including permission templates and child-agent upgrade plans that may grant broad access if used without review.

Mitigation: Keep permissions minimal, inspect every generated settings.local.json file, and review proposed child-agent changes before deployment.

Risk: The artifact discusses unattended scheduled agent runs and full-access permission templates, which can increase operational and data-access risk.

Mitigation: Avoid full-access templates, permission-skip modes, and unattended cron or launchd jobs until commands, paths, and schedules are explicitly reviewed.

## Reference(s):

- [Self-Evolving Agent Model](references/evo-agent-model.md)
- [Model Capability Levels and Permission Rules](references/model-capability.md)
- [settings.local.json Permission Template](references/settings.local.json.template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, generated skill files, configuration snippets, reports, and execution-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file-system changes, permission settings, scheduled tasks, and child-agent upgrade plans that require human review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
