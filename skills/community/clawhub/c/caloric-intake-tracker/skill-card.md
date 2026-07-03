## Description: <br>
Log and track daily calorie intake, macronutrients, body weight, and waist measurements locally in a SQLite database with granular statistics, weekly averages, and future calorie budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to log meals, calorie and macronutrient targets, body weight, waist circumference, and custom measurements into a local SQLite database. They can review daily breakdowns, weekly summaries, rolling trends, body-measurement reports, and future calorie budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calorie, weight, waist, and other body measurement data is stored in a local SQLite file that may expose sensitive health information if placed in a shared or synced directory. <br>
Mitigation: Use --database to place the database in a private directory, and avoid shared or synced folders when privacy matters. <br>
Risk: Existing health_data.db files can be changed by migrations and by update, delete, and measurement-type delete commands. <br>
Mitigation: Back up existing database files before first use or upgrades, and use list or stats day to identify entries before changing or deleting them. <br>


## Reference(s): <br>
- [Calorie Tracker ClawHub Skill Page](https://clawhub.ai/patello/skills/caloric-intake-tracker) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with inline shell commands and local SQLite state changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes health_data.db by default; --database can direct storage to another local SQLite file.] <br>

## Skill Version(s): <br>
1.4.2 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
