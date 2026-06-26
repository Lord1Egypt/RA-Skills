## Description: <br>
Physical performance routing for workouts, fitness tracking, nutrition, meal logging, macros, recipes, and intent routing to Coach, Chef, or Hevy sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to route physical health and performance requests to training, nutrition, and Hevy-backed fitness workflows. It supports workout summaries, progress analysis, meal logging, macro checks, recipes, meal plans, grocery lists, and RPG-style Body XP updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access sensitive workout, nutrition, and account data through local vault files and a Hevy API key. <br>
Mitigation: Install only when that access is acceptable, restrict the Hevy configuration file permissions, and avoid sharing API keys in chat or source files. <br>
Risk: The skill can write persistent meal logs, workout logs, RPG stats, calendar entries, and related vault files. <br>
Mitigation: Require confirmation before write operations and review generated file changes before relying on them. <br>
Risk: The Hevy setup path includes installer and configuration scripts. <br>
Mitigation: Review or replace the installer, verify the Hevy CLI binary independently, and inspect shell commands before execution. <br>


## Reference(s): <br>
- [Hevy API Docs](https://api.hevyapp.com/docs/) <br>
- [Hevy App](https://www.hevyapp.com/) <br>
- [Hevy Developer Settings](https://hevy.com/settings?developer) <br>
- [Hevy CLI Command Reference](hevy/references/api_commands.md) <br>
- [Hevy Data Structures](hevy/references/data_structures.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cylqqqcyl/body) <br>
- [Publisher Profile](https://clawhub.ai/user/cylqqqcyl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-oriented Hevy outputs, and structured vault file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local vault files and may use Hevy CLI JSON output when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
