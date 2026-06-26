## Description: <br>
Creates Feishu calendar events and optional Feishu video meetings through the Feishu Calendar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sangy12](https://clawhub.ai/user/sangy12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using Feishu can ask an agent to prepare calendar event API calls, choose required and optional fields from user input, and create meetings with Feishu video conferencing when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Feishu user token to create real calendar events and video meetings. <br>
Mitigation: Keep the token private, restrict access to the token file, and avoid printing the token in logs or chat. <br>
Risk: Incorrect meeting details could create an unintended calendar event or video meeting. <br>
Mitigation: Review the calendar ID, title, time, and video-meeting setting before sending the API request. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu calendar IDs, OAuth token handling steps, timestamps, request payloads, and meeting links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
