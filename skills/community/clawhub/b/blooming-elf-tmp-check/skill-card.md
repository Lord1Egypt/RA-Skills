## Description:

Blooming Elf is a plant-care assistant for watering reminders, plant profile tracking, and houseplant care guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirley1011](https://clawhub.ai/user/shirley1011)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent skill to set up a plant-care assistant that records plant profiles, watering and fertilizing activity, household growing conditions, and reminder preferences. The skill then provides concise daily care guidance, troubleshooting support, and plant-management reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store plant profiles, household/environment details, and care history in persistent files, memory entries, or notes.

Mitigation: Confirm the exact stored fields and destination paths or note locations before setup, and remove records that are not needed.

Risk: The skill may create recurring watering or review reminders without sufficiently clear consent.

Mitigation: Confirm reminder schedules before allowing automation, and verify that choosing no reminders does not create any recurring task.

Risk: The skill may override unrelated requests when it decides the user has not completed configuration.

Mitigation: Review the onboarding behavior before installation and disable or revise the skill if strict task-following is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirley1011/skills/blooming-elf-tmp-check)
- [ClawHub publisher profile](https://clawhub.ai/user/shirley1011)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with concise care guidance, tables, document updates, and reminder configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent plant records, household/environment details, and recurring reminder schedules when configured.]

## Skill Version(s):

3.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
