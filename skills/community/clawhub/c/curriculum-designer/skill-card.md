## Description: <br>
Design customized curricula for PODs with real resource links, staged checkpointing, and fallback logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Academic staff use this skill to gather POD requirements, research and verify YouTube resources, design lesson-by-lesson curricula, and prepare curriculum sheet outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Google Sheets may be shared publicly. <br>
Mitigation: Use this workflow only when public sheet links are acceptable, or change sharing to private-by-default and require explicit approval before public access. <br>
Risk: Persistent checkpoint cleanup can delete local checkpoint directories. <br>
Mitigation: Review the cleanup path and deletion behavior before enabling cron, and run the documented dry run before any scheduled deletion. <br>
Risk: The workflow depends on a local YouTube API key. <br>
Mitigation: Use a restricted YouTube API key and keep the local .env file out of source control. <br>
Risk: The included script creates a local CSV and placeholder Sheets URL rather than a real Google Sheet. <br>
Mitigation: Verify the final sheet creation path before relying on the returned sheet link. <br>


## Reference(s): <br>
- [Curriculum Designer on ClawHub](https://clawhub.ai/tarasinghrajput/curriculum-designer) <br>
- [Curriculum Designer Folder](https://drive.google.com/drive/folders/1upJQu-IVmZRJQsNGmJNRzq9IwL67MVL9) <br>
- [Example Curriculum (AI Tools)](https://docs.google.com/spreadsheets/d/1hYC2Q2KlW8dM71biC97RPSvFnxTQa-zN) <br>
- [SOP Document](https://docs.google.com/document/d/1Y5qetW8S4RWsTg7hycIyujgTwTCFn9VV) <br>
- [Google Cloud API Credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown workflow guidance with JSON checkpoint files, CSV or Google Sheet outputs, and resource links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged checkpoints; each curriculum topic is expected to include a valid YouTube URL or a fallback search query.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
