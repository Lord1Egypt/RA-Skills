## Description: <br>
Generate vintage comic-book style illustrations from topics, briefings, or meeting notes. Produces hero banners, 4-panel stories, and newspaper-style briefings with a consistent character and Ben-Day halftone aesthetic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adawodu](https://clawhub.ai/user/adawodu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn topics, briefings, meeting notes, or uploaded photos into vintage comic-style images, including hero banners, four-panel stories, and newspaper-style briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated media and prompt-derived context are sent to an external Convex service with limited disclosure or user control. <br>
Mitigation: Use only non-sensitive prompts and images unless the publisher documents upload, storage, retention, and approve-before-publish controls. <br>
Risk: The skill requires sensitive credentials through GEMINI_API_KEY. <br>
Mitigation: Provide credentials only through a trusted runtime environment and avoid exposing them in prompts, logs, or shared outputs. <br>
Risk: The workflow is designed to run shell commands and upload the result after collecting the topic. <br>
Mitigation: Review the prompt, generated file path, and upload destination before running in environments with access to private files or credentials. <br>


## Reference(s): <br>
- [Comic Brief on ClawHub](https://clawhub.ai/adawodu/comic-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Media links, Guidance] <br>
**Output Format:** [Text response with a MEDIA URL after generating a PNG image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and uploads generated PNG media to a Convex-backed media library.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
