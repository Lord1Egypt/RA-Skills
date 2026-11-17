## Description:

Fetches Edsby student data to generate grade reports, provide bi-weekly improvement summaries, and sync assignments to Google Calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lystea11](https://clawhub.ai/user/lystea11)

### License/Terms of Use:


## Use Case:

Students and education-support users use this skill to collect class, grade, and assignment information from Edsby, generate progress reports, and create Google Calendar due-date events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive school data and account credentials with too little user control and protection.

Mitigation: Review before installing, keep Google tokens and the Edsby browser profile out of shared folders and source control, and use secure credential storage.

Risk: Assignment sync can affect a user's primary Google Calendar.

Mitigation: Use a dedicated Google Calendar and grant the least Google OAuth scope possible.

Risk: Scheduled or repeated sync may create duplicate or unintended calendar events without confirmation controls.

Mitigation: Avoid scheduled or repeated sync until confirmation, duplicate prevention, and credential handling have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lystea11/skills/edsbygrades)

## Skill Output:

**Output Type(s):** [text, markdown, structured data, API calls]

**Output Format:** [Markdown reports, status strings, structured JavaScript objects, and Google Calendar event creation requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Edsby host configuration, Google OAuth credentials, a browser context path, and a Google Calendar target.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
