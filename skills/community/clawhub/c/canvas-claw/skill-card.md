## Description: <br>
Generate images and videos through AI-video-agent. Supports image create, image remix, video create, and video animate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toolok5](https://clawhub.ai/user/toolok5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use Canvas Claw to submit image and video generation jobs to a configured AI-video-agent service, including image creation, image remixing, text-to-video, and image-to-video flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, local media, passwords, and generated tokens may be sensitive when sent to or received from the configured remote service. <br>
Mitigation: Use only trusted AI-video-agent servers, prefer HTTPS endpoints, avoid exposing passwords or generated tokens in shell history or logs, and submit confidential prompts or media only to services approved for that data. <br>
Risk: Generated media and metadata are written to local output directories and may include task IDs, result URLs, prompts, provider names, and model IDs. <br>
Mitigation: Review generated files and metadata before sharing, committing, or publishing output directories. <br>


## Reference(s): <br>
- [Canvas Claw ClawHub Page](https://clawhub.ai/toolok5/canvas-claw) <br>
- [Canvas Claw Installation Guide](artifact/INSTALL.md) <br>
- [Canvas Claw Skill Definition](artifact/SKILL.md) <br>
- [Canvas Claw Design Notes](artifact/docs/plans/2026-04-07-canvas-claw-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Files, JSON] <br>
**Output Format:** [Markdown instructions and Python CLI output, with generated media files and metadata.json result bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured AI-video-agent endpoint, token, and site ID.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
