## Description:

Give Hermes Agent real phone capabilities through Amber's Twilio/OpenAI voice bridge and MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batthis](https://clawhub.ai/user/batthis)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Operators use Amber through Hermes to screen inbound calls, place outbound calls after explicit confirmation, review call history, resolve contacts, and coordinate calendars or opt-in CRM follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a suspicious verdict at medium confidence and says its analysis was partial; its summary highlights installation setup and resource use for review.

Mitigation: Before installing, review CRM consent and transcript-enrichment settings, the optional background watcher, granted host and MCP permissions, network access, and how credentials and call data are protected.

Risk: The skill handles real calls and sensitive caller, contact, calendar, and transcript data, and calls may incur provider and API charges.

Mitigation: Confirm the recipient and objective before dialing; configure caller notice, consent, access controls, retention, and deletion practices before using it with real callers.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/batthis/skills/amber-phone-agent)
- [Amber project setup and documentation (link declared in skill metadata)](https://github.com/batthis/amber-openclaw-voice-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions may lead to real calls or calendar changes; the skill requires explicit confirmation for outbound calls and calendar creation.]

## Skill Version(s):

5.5.66 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
