## Description: <br>
Create and check long-running video material evaluation tasks for submitted videos, including task creation, task listing, and task-detail retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local MP4 video materials for long-running evaluation tasks, then query task status and results later. It is intended for material or creative-asset evaluation workflows, not generic video storage or upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key and sends selected video materials and prompts to Volcengine services. <br>
Mitigation: Confirm the user is comfortable with the external transfer and credential use before running task submission commands. <br>
Risk: Submitting evaluation tasks may create API cost or long-running work. <br>
Mitigation: Prefer explicit confirmation before starting generation or evaluation jobs and return the task ID so the user can check status later. <br>
Risk: Unsupported files or oversized batches can cause failed submissions. <br>
Mitigation: Validate MP4 format, video/mp4 MIME type, 50 MB per-file size, and the 50-video batch limit before uploading any file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-airesearch-videoeval) <br>
- [Volcengine API key console](https://console.volcengine.com/datatester/ai-research/audience/list?tab=apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Human-readable Markdown summaries backed by JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task submission is non-blocking; detail output summarizes completed task results and avoids raw implementation fields unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
