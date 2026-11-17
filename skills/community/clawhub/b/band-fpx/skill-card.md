## Description:

Read BAND (band.us) group data from a shell — your bands, a band's posts and announcements, a post's comments, notices, post search, calendar events (schedules), members, chat channels with their latest message, and unread news counts — through the user's signed-in band.us browser session with the fpx CLI. Use when asked about a BAND group, its posts, upcoming events/calendar, who is in a band, chats, or what's new on BAND.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and BAND users use this skill to retrieve read-only group feeds, notices, events, member lists, chat channel previews, and unread counts from their signed-in BAND account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overriding the API destination while authenticated BAND session cookies are sent could expose account credentials.

Mitigation: Before installing, check the API destination configuration and do not use an untrusted override with a signed-in BAND session.

Risk: The security scan inspected only 2 of the 3 components, so its evidence is incomplete.

Mitigation: Review the complete skill release before installation, including the component that was not inspected by the scan.

## Reference(s):

- [BAND recipes](references/recipes.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only group data; chat access is limited to each channel's latest message.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
