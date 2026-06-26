## Description: <br>
Generate AI videos and images via Chenyu Studio AIGC API, including text-to-video, image-to-video, video extension, style transfer, and AI image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dionren](https://clawhub.ai/user/dionren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to discover Chenyu Studio AIGC recipes, submit text, image, video, audio, and reference-based generation tasks, poll outputs, and manage task lifecycle through the API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, videos, and task metadata are submitted to the third-party Chenyu Studio API. <br>
Mitigation: Install only if the publisher and service are trusted, verify CHENYU_BASE_URL before use, prefer a scoped API key if available, and avoid sending sensitive local media. <br>
Risk: Local media may be encoded into temporary JSON payload files for upload. <br>
Mitigation: Use a private temporary file instead of a shared /tmp/payload.json path and delete it after submission. <br>
Risk: Task-management commands can cancel or delete generation jobs when given a task ID. <br>
Mitigation: Confirm task IDs and task status before canceling or deleting completed tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dionren/chenyu-aigc) <br>
- [Chenyu Studio API base URL](https://chenyu.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request examples for recipe discovery, schema inspection, execution, polling, cancellation, listing, and deletion.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
