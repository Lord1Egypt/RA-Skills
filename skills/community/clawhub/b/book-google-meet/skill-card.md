## Description: <br>
Create scheduled Google Calendar events with OPEN access Google Meet spaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KumaDun](https://clawhub.ai/user/KumaDun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create scheduled Google Calendar events with Google Meet links, optional attendees and descriptions, and configurable Meet access settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad Google Calendar and Meet authority. <br>
Mitigation: Authorize it only for accounts where creating and modifying calendar events and Meet spaces is acceptable, and consider a dedicated Google account or narrower OAuth scopes. <br>
Risk: Meetings are created with OPEN access by default. <br>
Mitigation: Use TRUSTED or RESTRICTED access for private or sensitive meetings. <br>
Risk: The skill writes reusable OAuth tokens to meeting_token.pickle. <br>
Mitigation: Protect the token file, never share or commit it, and delete it when it is no longer needed. <br>
Risk: Credential or token files supplied by another party could expose or redirect authorization. <br>
Mitigation: Use credentials generated from your own Google Cloud project and do not use token or credential files supplied by someone else. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/KumaDun/book-google-meet) <br>
- [Google Calendar API](https://developers.google.com/calendar/api/v3/reference) <br>
- [Google Meet API](https://developers.google.com/workspace/meet/api/reference/rest) <br>
- [Meet spaces.get](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/get) <br>
- [Meet spaces.patch](https://developers.google.com/workspace/meet/api/reference/rest/v2/spaces/patch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with Google Calendar and Meet resource links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or modifies Google Calendar events and Google Meet spaces, and writes an OAuth token cache when authorized.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
