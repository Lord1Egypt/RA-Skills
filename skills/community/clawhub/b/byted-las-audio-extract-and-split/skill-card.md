## Description: <br>
Extracts audio tracks from common video files and splits video or audio into fixed-length segments using Volcengine LAS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare media-processing jobs that extract audio from video, upload local inputs to TOS when needed, split audio into timed segments, estimate cost, and present output paths after processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected media to Volcengine LAS/TOS for processing. <br>
Mitigation: Use only media the user is permitted to send to Volcengine services, and confirm the target region matches the API key and TOS bucket before upload. <br>
Risk: The setup script can automatically download and install remote SDK code. <br>
Mitigation: Review or pin the SDK artifact before running initialization, and install in an isolated virtual environment. <br>
Risk: The workflow requires sensitive credentials such as LAS_API_KEY and may require Volcengine access keys for downloading TOS output. <br>
Mitigation: Use least-privilege temporary credentials, avoid committing secrets to project files, and prefer environment variables or short-lived local shell configuration. <br>
Risk: Processing can incur Volcengine charges. <br>
Mitigation: Calculate an estimated price from media duration and require explicit user confirmation before upload or execution. <br>


## Reference(s): <br>
- [las_audio_extract_and_split API Reference](references/api.md) <br>
- [Pricing Reference](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-las-audio-extract-and-split) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON payloads, and result tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LAS credentials and explicit user confirmation after price estimation before job execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
