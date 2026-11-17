## Description:

Read Google Calendar from the local host using the configured gog wrapper for agenda, schedule, upcoming appointment, and calendar summary requests on a configured OpenClaw host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgf78](https://clawhub.ai/user/jgf78)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to retrieve and summarize Google Calendar events from a configured OpenClaw host for daily agendas, weekly events, upcoming appointments, and calendar summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the configured host Google Calendar through local credentials, including from Telegram or shared chat deployments, without an explicit authorization step.

Mitigation: Install only on trusted OpenClaw hosts and restrict triggering chat channels to users authorized to view the configured calendar; consider adding confirmation or authorization before returning events.

Risk: Calendar access depends on the local wrapper, the GOG_KEYRING_PASSWORD environment variable, and an available local Google token or keyring.

Mitigation: Confirm the OpenClaw service environment and keyring are available before relying on the skill, and report credential or keyring failures plainly instead of re-running OAuth setup by default.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise natural language or Markdown agenda summaries, with local shell wrapper commands used by the agent when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can group all-day events, timed events, and birthdays or tasks when useful.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
