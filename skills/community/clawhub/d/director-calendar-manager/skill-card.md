## Description: <br>
Manage calendar availability, schedule meetings across timezones, find optimal meeting times, and send calendar invites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[di5cip1e](https://clawhub.ai/user/di5cip1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People coordinating meetings use this skill to find available time slots, compare timezone-aware options, and prepare calendar invitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar invites may be sent with incorrect recipients, dates, titles, descriptions, or notification settings. <br>
Mitigation: Draft invites first and require explicit user confirmation of attendees, timing, title, description, and external email notifications before sending. <br>
Risk: Timezone conversion or availability assumptions may produce unsuitable meeting options. <br>
Mitigation: Show proposed times with timezone context and ask the user to confirm the selected slot before generating or sending an invite. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with optional Python and ICS snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed meeting times, timezone conversions, and calendar invite content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
