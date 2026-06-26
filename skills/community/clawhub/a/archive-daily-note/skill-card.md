## Description: <br>
Automatically moves yesterday's Obsidian daily note into a past-days/ archive folder using the Obsidian CLI move command to preserve wiki-links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madebydia](https://clawhub.ai/user/madebydia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Obsidian users and automation operators use this skill to archive the previous day's daily note into a past-days folder while preserving wiki-links through the Obsidian CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify files in an Obsidian vault by moving a daily note and allowing obsidian move to update internal links. <br>
Mitigation: Run it only in the intended vault after confirming the daily note naming format and the past-days folder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/madebydia/archive-daily-note) <br>
- [Publisher profile](https://clawhub.ai/user/madebydia) <br>
- [Project homepage](https://github.com/madebydia/archive-daily-note) <br>
- [OpenClaw](https://openclaw.app) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify files in the active Obsidian vault by moving one daily note and updating internal links through obsidian move.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
