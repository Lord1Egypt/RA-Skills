## Description:

blooming-elf（绽放精灵）—— 智能浇花浇水提醒与植物绿植花卉养护助手

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirley1011](https://clawhub.ai/user/shirley1011)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a plant-care assistant to create plant records, track watering and care activity, receive user-confirmed reminders, and get concise troubleshooting guidance for household plants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores household context, schedules, file paths, and document IDs in shared plaintext agent memory.

Mitigation: Use a dedicated local folder or tightly scoped knowledge base, avoid storing unnecessary household details, and periodically review or delete the memory configuration.

Risk: The skill can create reminder automations after user confirmation.

Mitigation: Review scheduled reminders periodically and cancel or adjust automations that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shirley1011/skills/blooming-elf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown responses with tables, templates, and concise care instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update plant record files, memory configuration, document entries, and user-confirmed reminder schedules when the host agent provides those capabilities.]

## Skill Version(s):

3.1.3 (source: server release metadata; artifact frontmatter reports 3.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
