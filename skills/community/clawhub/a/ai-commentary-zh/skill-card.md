## Description: <br>
面向解说/讲解场景的 Sparki skill 变体，沿用最新版官方 Sparki 安装、API key、上传和命令说明，同时保留 commentary 场景定位。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to turn source videos into clearer commentary, explainer, reaction, or narrated videos with stronger structure and storytelling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, filenames, prompts, and edit metadata are uploaded to Sparki for remote processing. <br>
Mitigation: Install only when that data sharing is acceptable, review selected inputs before upload, and keep the default Sparki endpoint unless another endpoint is intentionally trusted. <br>
Risk: API keys may be stored in the OpenClaw config file when setup is used. <br>
Mitigation: Prefer SPARKI_API_KEY for transient credentials or protect the OpenClaw config directory when saving keys locally. <br>
Risk: Generated videos are written to a local workspace path and may overwrite or expose expected output locations if not reviewed. <br>
Mitigation: Review output paths before downloading results and restrict workspace access to intended users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-commentary-zh) <br>
- [Sparki homepage](https://sparki.io) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected video files to Sparki for remote processing and can download generated video files to the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
