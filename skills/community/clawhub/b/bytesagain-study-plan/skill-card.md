## Description:

Create study plans for exams with schedules and reminders. Use when adding tasks, planning reviews, tracking progress, prioritizing subjects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and study planners use this skill to generate Chinese-language exam preparation plans, daily study schedules, review intervals, pomodoro plans, and simple local task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated study schedules may be incomplete, unrealistic, or mismatched to the learner's actual exam requirements.

Mitigation: Review generated plans before relying on them and adjust study hours, subjects, milestones, and review intervals for the learner's curriculum and constraints.

Risk: The local task logger stores simple study-plan data files under the configured data directory.

Mitigation: Use the STUDY_PLAN_DIR setting when a specific storage location is required and review local data files before sharing or deleting the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-study-plan)
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like terminal text with schedules, checklists, reminders, and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language study planning output; local task logger writes simple data files under the configured study-plan data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
