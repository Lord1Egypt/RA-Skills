## Description: <br>
Parse and sync flomo exported HTML data to an Obsidian vault with attachment support, one-time manual export conversion, and automatic sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perseveringman](https://clawhub.ai/user/perseveringman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to import Flomo exports into Obsidian, preserve tags and attachments, and optionally configure recurring sync from Flomo to an Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle Flomo credentials or browser session material. <br>
Mitigation: Prefer manual export or safe mode, never paste a Flomo password into chat, and treat .env and flomo_browser_data as sensitive account-access material. <br>
Risk: The skill can read Flomo account data and write into the target Obsidian vault. <br>
Mitigation: Run it only for vaults and accounts you intend to sync, and review the target output path before execution. <br>
Risk: Automatic sync setup can create ongoing scheduled jobs. <br>
Mitigation: Review any cron or scheduled task command, frequency, output path, and logging destination before enabling it. <br>


## Reference(s): <br>
- [Flomo web app](https://flomoapp.com) <br>
- [ClawHub skill page](https://clawhub.ai/perseveringman/flomo-to-obsidian) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/perseveringman) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script invocations, and generated Obsidian markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Obsidian vault files, attachment folders, sync state, browser session data, and optional scheduled tasks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
