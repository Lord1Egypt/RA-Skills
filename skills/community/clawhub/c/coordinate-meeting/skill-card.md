## Description: <br>
Coordinates group meeting scheduling by creating a MeetLark poll, sharing the participation link, collecting votes, and reporting the best time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkelk](https://clawhub.ai/user/mkelk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and their agents use this skill to create a scheduling poll, share it with participants, check vote status, and close the poll once a meeting time is selected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting purpose, proposed times, participant-related details, and verification email information are sent to MeetLark. <br>
Mitigation: Confirm the user is comfortable sharing these details with meetlark.ai and include only the information needed to coordinate the meeting. <br>
Risk: The admin token can be used to check results and close the poll. <br>
Mitigation: Keep the admin token private and do not include it in messages sent to participants. <br>
Risk: Anyone with the participation link may be able to vote in the poll. <br>
Mitigation: Share the participation link only with intended voters through the user's chosen communication channel. <br>


## Reference(s): <br>
- [MeetLark API Documentation](https://meetlark.ai/docs) <br>
- [MeetLark OpenAPI Specification](https://meetlark.ai/api/v1/openapi.json) <br>
- [MeetLark](https://meetlark.ai) <br>
- [ClawHub Listing](https://clawhub.ai/mkelk/coordinate-meeting) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with API request examples, scheduling summaries, and user-facing message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes participation URLs, vote summaries, recommended meeting times, and confirmation-message guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
