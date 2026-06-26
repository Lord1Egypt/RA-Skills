## Description: <br>
Use Chanjing Avatar API for lip-syncing video generation by uploading audio or video, creating tasks, and polling for results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate Chanjing Avatar lip-sync video creation, including media upload, task creation, task polling, and retrieval of generated video URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Chanjing credentials and persists access tokens in a local credentials.json file. <br>
Mitigation: Store credentials.json in a protected local directory, use CHANJING_OPENAPI_CREDENTIALS_DIR when needed, and do not commit credentials.json to version control. <br>
Risk: The skill uploads user-selected media to Chanjing for lip-sync video processing. <br>
Mitigation: Upload only media you are comfortable sending to Chanjing and keep the API base URL on the official Chanjing endpoint. <br>
Risk: Generated video result URLs may be returned by the API and downloaded or shared by the agent workflow. <br>
Mitigation: Review returned video URLs and generated media before downloading, storing, or sharing them outside the workspace. <br>


## Reference(s): <br>
- [Chanjing API Documentation](https://doc.chanjing.cc) <br>
- [Chanjing File Management API](https://doc.chanjing.cc/api/file/file-management.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/binkes/chanjing-avatar) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands; scripts return JSON, file IDs, task IDs, and video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads user-selected media to Chanjing, persists access tokens in credentials.json, and polls asynchronous video-generation tasks.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
