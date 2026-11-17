## Description:

Tracks daily calorie and protein intake, calorie goals, food entries, and weight logs in a local SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnqso](https://clawhub.ai/user/cnqso)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to record meals, estimate protein when needed, view daily calorie progress, manage goals, and log weight history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diet and weight records are stored automatically in a local plaintext SQLite database.

Mitigation: Use the skill only in a trusted private workspace and review where calorie_data.db is stored before logging sensitive information.

Risk: Command templates include user-supplied food names.

Mitigation: Pass arguments without a shell or apply robust escaping before using the skill with untrusted food text.

Risk: Broad food-related phrasing may cause the agent to invoke the skill when a user is only discussing food.

Mitigation: Confirm ambiguous food or weight entries before logging them.

## Reference(s):

- [Calorie Counter on ClawHub](https://clawhub.ai/cnqso/skills/calorie-counter)
- [Publisher profile](https://clawhub.ai/user/cnqso)
- [README](artifact/README.md)
- [Quick Start](artifact/QUICK_START.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local SQLite database named calorie_data.db.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
