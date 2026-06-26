## Description: <br>
面向 faceless/no-face 场景的 Sparki skill 变体，沿用最新版官方 Sparki 安装、API key、上传和命令说明，同时保留 faceless 场景定位。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create faceless, automation-style, narration-led videos through Sparki's cloud video editing workflow. It is aimed at no-face explainers, short-form clips, captions, montages, vlog edits, and prompt-driven video processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video files are uploaded to Sparki for processing. <br>
Mitigation: Use the skill only with videos that are appropriate to send to Sparki, and avoid confidential content unless the service is trusted for that data. <br>
Risk: A Sparki API key can be provided through SPARKI_API_KEY or saved locally. <br>
Mitigation: Prefer environment-based key handling where possible, protect local configuration files, and rotate the key if it may have been exposed. <br>
Risk: Changing the default Sparki endpoint can send data to an unintended service. <br>
Mitigation: Keep the default endpoint unless there is a deliberate and reviewed reason to override it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/faceless-video-zh) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI responses are JSON and completed edits download as video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sparki API key; accepts local MP4 or MOV inputs up to 3GB each and writes results under the configured OpenClaw workspace unless an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
