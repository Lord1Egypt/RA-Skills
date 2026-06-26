## Description: <br>
Camera API helps agents query camera device lists, resolve device IDs, check thumbnails and online status, summarize cloud events by date, inspect event details, and trigger a user-requested screenshot workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyfinec](https://clawhub.ai/user/flyfinec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate authorized camera cloud API workflows from an agent, including device lookup, current status checks, event summaries, thumbnails, and requested screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access camera account data and may trigger a new camera screenshot when the user asks for a current view. <br>
Mitigation: Install it only for camera accounts and devices the user owns or is authorized to access, and treat current-view requests as active screenshot operations. <br>
Risk: Camera API credentials can expose private device and event data if shared in chat or hardcoded. <br>
Mitigation: Keep TIVS_API_KEY and TIVS_APP_ID in environment configuration and do not paste or embed secrets in prompts, skill text, code, or responses. <br>
Risk: Signed camera image URLs may expose private media if returned directly. <br>
Mitigation: Download and display image content when possible, and avoid sending raw signed image URLs as final user-facing output. <br>


## Reference(s): <br>
- [ClawHub Camera API release](https://clawhub.ai/flyfinec/camera-api) <br>
- [flyfinec publisher profile](https://clawhub.ai/user/flyfinec) <br>
- [Camera cloud API endpoint](https://openapi-cn01.tange365.com/) <br>
- [icam365 API key page](https://skill.webcamapp.cc/icam365/api-key) <br>
- [wosee API key page](https://skill.webcamapp.cc/wosee/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown response with summarized camera status, event details, and image-display guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TIVS_API_KEY and TIVS_APP_ID from environment configuration; does not expose raw signed image URLs to users.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
