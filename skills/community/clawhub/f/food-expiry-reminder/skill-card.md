## Description:

Tracks food items in a local JSON inventory and helps agents add records, list stored foods, check expiry status, and surface one-week expiry reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unlimitwave](https://clawhub.ai/user/unlimitwave)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to maintain a local household food inventory, calculate expiry dates from production dates and shelf-life values, and produce reminders for expired or soon-to-expire items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual edits or deletions can damage or remove the local food inventory JSON file.

Mitigation: Back up data/food_data.json before manual edits or deletions.

Risk: The documented cron setup creates recurring daily reminders if installed.

Mitigation: Add the cron job only when recurring local reminders are intentional.

## Reference(s):

- [Data Structure](references/data_structure.md)
- [Usage Examples](references/examples.md)
- [FAQ](references/faq.md)
- [ClawHub Skill Page](https://clawhub.ai/unlimitwave/skills/food-expiry-reminder)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-backed local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local data/food_data.json storage and Python standard-library scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
