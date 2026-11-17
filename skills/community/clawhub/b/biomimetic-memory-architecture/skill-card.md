## Description:

Install, verify, and manage OpenClaw memory with integrated daily distillation, weekly synthesis, procedural learning, retention, and cold archiving workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to install, verify, and maintain a structured memory system that consolidates daily activity, captures procedural lessons, audits aged records, and moves compressed long-term records to cold archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent daily and weekly automation can write to private memory over time.

Mitigation: Review installed cron jobs and disable or remove default schedules when autonomous memory writes are not desired.

Risk: Phase 2 retention execution can rewrite references and move memory files into cold archive.

Mitigation: Run and inspect the read-only audit and dry-run output before using Phase 2 with --execute.

Risk: The release security summary flags under-scoped approval and path-safety concerns around private memory movement.

Mitigation: Review every affected path in the audit report and only execute migration in trusted workspaces.

## Reference(s):

- [BMA Architecture Reference](references/architecture.md)
- [BMA Installation and Integration](references/installation.md)
- [BMA Daily Memory Distillation](references/daily-distillation.md)
- [Weekly Synthesis Instructions](references/weekly-synthesis.md)
- [BMA Retention Rubric](references/retention-rubric.md)
- [Lesson-Imprint Component](references/lesson-imprint.md)
- [OpenCortex Foundation Inside BMA](references/opencortex-foundation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands, configuration instructions, and generated memory or audit files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify workspace memory files, cron jobs, vault state, metrics, retention reports, and cold archives when installation or execution commands are run.]

## Skill Version(s):

0.1.7 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
