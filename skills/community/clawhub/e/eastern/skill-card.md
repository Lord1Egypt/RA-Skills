## Description:

Summarizes public China Eastern Airlines flight, check-in, announcement, and news information without supporting booking or account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect concise summaries of public China Eastern Airlines routes, schedules, check-in requirements, announcements, and news items for internal analysis and reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use beyond public website summarization could expose account, booking, payment, or private travel data workflows that were not reviewed for this release.

Mitigation: Restrict use to public China Eastern Airlines pages unless a separate authorization and security review covers private or transactional workflows.

Risk: Dynamic public pages and schedule notices can change, making extracted summaries stale or incomplete.

Mitigation: Wait for page loading to complete, preserve source links in summaries, and have users verify time-sensitive flight or policy information against the source page.

## Reference(s):

- [China Eastern Airlines website](https://www.ceair.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/eastern)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public website information only; excludes account login, booking, payment, and private travel data handling.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
