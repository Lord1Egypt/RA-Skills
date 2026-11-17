## Description:

Dayplanner is a command-line planner for recording tasks, plans, reviews, streaks, reminders, priorities, and exports in local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage lightweight day planning, task notes, habits, reminders, reviews, and local exports from a shell environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planner entries are stored as plaintext local files and may expose private tasks, meetings, or reminders on shared machines.

Mitigation: Avoid entering credentials or highly sensitive work details and verify local file permissions before use.

Risk: CSV, JSON, and TXT exports may carry sensitive planner data or malformed entry content into downstream tools.

Mitigation: Review and sanitize exports before sharing them or opening them in spreadsheet and analysis tools.

Risk: The skill behaves as a simple local logging tool, not a full calendar scheduler.

Mitigation: Use it for lightweight planning notes and verify critical deadlines or meetings in a dedicated scheduling system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/dayplanner)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Command-line text output with local JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores planner entries as plaintext files under ~/.local/share/dayplanner.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
