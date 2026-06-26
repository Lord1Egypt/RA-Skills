## Description: <br>
Manage Cal.com calendars via CLI, including schedules, bookings, event types, available slots, and user profile tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Cal.com accounts from an agent-driven CLI: inspect schedules, bookings, event types, slots, and profile data, then perform calendar-management actions when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote install commands could fetch and run code from the GitHub/api2cli installation path. <br>
Mitigation: Review the install source before running setup commands and install only when the agent should manage the user's Cal.com account. <br>
Risk: The Cal.com token is stored at ~/.config/tokens/calcom-cli.txt. <br>
Mitigation: Use a least-privilege or revocable token and protect or remove the token file when the skill is no longer needed. <br>
Risk: Calendar mutations can cancel bookings or delete schedules and event types. <br>
Mitigation: Ask the agent to confirm before destructive booking, schedule, or event-type actions. <br>


## Reference(s): <br>
- [Calcom Cli on ClawHub](https://clawhub.ai/Melvynx/calcom-cli) <br>
- [Bun installer](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with CLI command examples and JSON response envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agent-driven CLI calls to use --json for parseable results.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
