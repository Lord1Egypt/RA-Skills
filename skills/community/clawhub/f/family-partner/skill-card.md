## Description: <br>
Family Partner is an AI-powered OpenClaw family assistant suite for managing calendars, tasks, shopping, family memories, household labor, anniversaries, votes, milestones, challenges, and morning briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-PlusPlus](https://clawhub.ai/user/AI-PlusPlus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and families use this skill to organize household schedules, tasks, memories, family events, shopping needs, and shared decision-making through an OpenClaw assistant backed by a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and may resurface sensitive family details, including allergies, medical notes, school information, relationship context, and child-related household records. <br>
Mitigation: Review before installing; avoid entering highly sensitive child, health, school, or relationship details unless needed, and prefer explicit user confirmation before saving or resurfacing personal memories. <br>
Risk: Broad triggers such as greetings or memory requests may reveal personal briefings or stored household information unexpectedly. <br>
Mitigation: Require clear user intent before displaying personal briefings, and confirm the audience before showing calendar, task, anniversary, or memory summaries. <br>
Risk: All household records are kept in a local SQLite database that depends on the user's device security and backup practices. <br>
Mitigation: Limit database file access, use local device protections, and back up or delete the database according to household privacy needs. <br>


## Reference(s): <br>
- [ClawHub Family Partner release page](https://clawhub.ai/AI-PlusPlus/family-partner) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [ClawHub skill format specification](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) <br>
- [SQLite documentation](https://www.sqlite.org/docs.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with natural-language responses and inline SQLite shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sqlite3 to read and write a local family database at ~/.openclaw/family-partner/family.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
