## Description: <br>
Reads Google Calendar events from the local host through a configured wrapper and summarizes agendas for today, this week, upcoming days, or broader calendar requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgf78](https://clawhub.ai/user/jgf78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to answer agenda, schedule, upcoming appointment, and calendar-summary questions by reading the configured local Google Calendar wrapper and returning concise grouped summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent ongoing access to private calendar data through a local credentialed wrapper. <br>
Mitigation: Install only on trusted hosts, verify the calendar.sh wrapper and target Google account before use, and limit access to calendars appropriate for agent-assisted summaries. <br>
Risk: Calendar details may be summarized through connected chat surfaces, including Telegram. <br>
Mitigation: Avoid using the skill for sensitive calendars unless the user accepts disclosure through the connected chat channel. <br>
Risk: The wrapper depends on local keyring credentials and GOG_KEYRING_PASSWORD. <br>
Mitigation: Protect the runtime environment, keep credentials out of shared logs or prompts, and treat keyring failures as authorization failures rather than prompting broad reconfiguration. <br>


## Reference(s): <br>
- [Calendar Local on ClawHub](https://clawhub.ai/jgf78/calendar-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain-text or Markdown agenda summaries with brief shell-command and failure-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local calendar.sh wrapper with GOG_KEYRING_PASSWORD and may summarize all-day events, timed events, birthdays, tasks, or no-match results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
