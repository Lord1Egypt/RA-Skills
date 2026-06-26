## Description: <br>
Submits Dataify tasks that collect YouTube audio files by URL and returns the resulting task ID and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit YouTube audio collection jobs to Dataify with a YouTube URL, shared audio options, and a Dataify API TOKEN. It helps confirm parameters, handle token setup, submit the task, and report the task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided YouTube URLs and audio options are sent to Dataify to create collection tasks. <br>
Mitigation: Review the parameters before submission and avoid sending private or sensitive YouTube URLs unless the user is comfortable sharing them with Dataify. <br>
Risk: The workflow uses a Dataify API TOKEN and may guide the user to save it locally. <br>
Mitigation: Use a provided or locally configured DATAIFY_API_TOKEN only for this workflow, and save it locally only after explicit user confirmation. <br>
Risk: Incorrect URL, dropdown, direction, or file-name values can cause task submission failures. <br>
Mitigation: Validate YouTube URL format, allowed dropdown values, kilohertz and bitrate directions, and non-empty file names before submitting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-youtube-audio-by-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, JSON] <br>
**Output Format:** [Markdown parameter confirmations with inline shell commands and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task_id, status, submitted parameters, shared audio options, file name, dashboard URL, and a status message after successful submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
