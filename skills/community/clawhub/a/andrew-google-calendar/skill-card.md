## Description: <br>
Helps an agent list, create, update, and delete Google Calendar events through the Google Calendar API with OAuth 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibluewind](https://clawhub.ai/user/ibluewind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who want agent assistance with Google Calendar use this skill to inspect calendars and manage events after granting OAuth access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google Calendar OAuth with read/write calendar access, so misuse or an over-broad grant can expose or modify calendar data. <br>
Mitigation: Install only when comfortable granting that access, review calendar-changing actions before running them, and revoke the OAuth grant when access is no longer needed. <br>
Risk: OAuth credentials and tokens are stored in local home-directory files. <br>
Mitigation: Keep ~/.google-credentials.json and ~/.google-calendar-token.pickle private, use the skill on a trusted machine, and delete the token file if local access should be removed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ibluewind/andrew-google-calendar) <br>
- [Google Cloud Console API credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials and stores a local calendar token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
