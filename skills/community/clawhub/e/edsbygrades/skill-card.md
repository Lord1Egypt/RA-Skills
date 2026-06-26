## Description: <br>
Fetches Edsby student data to generate grade reports, provide bi-weekly summaries with tips, and sync assignments to Google Calendar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lystea11](https://clawhub.ai/user/Lystea11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students or their supporting agents use this skill to pull Edsby classes, grades, and assignments, produce student-facing grade reports and improvement summaries, and place assignment due dates on Google Calendar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private student records from an authenticated Edsby session. <br>
Mitigation: Use a dedicated browser profile, limit access to trusted users, and avoid exposing session state or fetched grade and assignment data. <br>
Risk: The skill can create Google Calendar events using persistent credentials. <br>
Mitigation: Review Google OAuth scopes, prefer a separate calendar, protect or avoid plaintext token files, and revoke credentials when no longer needed. <br>
Risk: Repeated daily sync may create duplicate or unwanted calendar events because deduplication and cleanup behavior is not clearly documented. <br>
Mitigation: Review calendar changes after initial runs and avoid repeated scheduled sync until duplicate-event and revoke behavior is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lystea11/edsbygrades) <br>
- [Publisher profile](https://clawhub.ai/user/Lystea11) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, plain text status messages, Google Calendar event writes, and structured Edsby data objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Edsby browser session state and Google Calendar credentials configured through environment variables and local token files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
