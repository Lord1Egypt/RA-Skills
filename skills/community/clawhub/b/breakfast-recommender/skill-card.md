## Description:

智能早餐推荐助手，根据冰箱食材推荐早餐、管理食材、记录偏好与历史。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophiayuan1984-jpg](https://clawhub.ai/user/sophiayuan1984-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this Chinese-language assistant to maintain a local fridge list, record dietary preferences, avoid repeating recent breakfast suggestions, and receive simple breakfast recommendations from available ingredients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replacing the full fridge list can overwrite prior stored ingredients when the user provides a complete new list.

Mitigation: Confirm that the user intends to replace the existing fridge list before writing a full-list update.

Risk: A recurring breakfast reminder can continue scheduled agent turns until cancelled.

Mitigation: Create recurring reminders only after an explicit user request and tell the user how to cancel them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophiayuan1984-jpg/skills/breakfast-recommender)
- [fridge.md](references/fridge.md)
- [history.md](references/history.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown tables and concise Chinese-language recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local fridge, preference, and recommendation-history files; may propose a recurring breakfast reminder when requested.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
