## Description: <br>
Google Sheets-driven employee reminder and special-event reporting workflow for internal operations. Use when setting up or migrating birthday reminders, daily management reports, Telegram/Discord reminder routing, Google Sheets staff/event schemas, or scheduled reporting jobs that read Sheets and send summaries into team chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vt-mmm](https://clawhub.ai/user/Vt-mmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal operations staff and developers use this skill to configure, test, migrate, and run a Google Sheets-based employee birthday and special-event reminder workflow that posts daily summaries to Telegram or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live-looking default Google Sheet, Google account, and Discord channel settings could send employee data to the wrong destination if reused without review. <br>
Mitigation: Set PLAN_A_SHEET_ID, GOG_ACCOUNT, DISCORD_CHANNEL_ID, and DISCORD_BOT_TOKEN for the target environment; run preview/json first; use a test channel and non-production data before prod-send or scheduler use. <br>
Risk: Employee birthdays, department data, and special-event details may be sent to the selected chat service. <br>
Mitigation: Confirm organizational approval for the chosen chat destination and disable PLAN_A_INCLUDE_INVALID_DETAILS unless detailed invalid-row reporting is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vt-mmm/employee-reminder-ops) <br>
- [Publisher profile](https://clawhub.ai/user/Vt-mmm) <br>
- [Plan A architecture](references/architecture.md) <br>
- [Deployment guide](references/deployment.md) <br>
- [Google Sheet schema](references/google-sheet-schema.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Windows deployment notes](references/windows.md) <br>
- [macOS deployment notes](references/macos.md) <br>
- [Plan A demo usage](references/PLAN_A_DEMO_USAGE.md) <br>
- [Plan A test plan](references/PLAN_A_TEST.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, and JavaScript workflow scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce preview text, JSON report details, Discord sends, scheduler guidance, and local state files when run by an agent with the required tools and credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
