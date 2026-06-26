## Description: <br>
Guides agents through using the newtranx CLI to upload MP4 videos, submit translation jobs, check results, and retrieve translated videos, subtitles, and speaker metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxj127](https://clawhub.ai/user/wxj127) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operations teams use this skill to translate MP4 videos or podcasts through the newtranx API from local files or HTTP URLs, then retrieve translated video output, subtitle files, and speaker metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs and runs an external npm package and sends video media to a third-party API. <br>
Mitigation: Install only when the `newtranx-ai` package and newtranx service are trusted, and review provider privacy and retention practices before uploading sensitive media. <br>
Risk: The CLI stores a temporary local token that could be exposed on shared or poorly protected machines. <br>
Mitigation: Use the skill on trusted machines, protect the local configuration file, and remove or refresh the token when access is no longer needed. <br>
Risk: Inputs are limited to MP4 videos with documented size and duration limits. <br>
Mitigation: Transcode unsupported formats to MP4 and confirm files are within the 5GB and 4-hour limits before upload. <br>


## Reference(s): <br>
- [AI Video Translation on ClawHub](https://clawhub.ai/wxj127/ai-video-translation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command sequences for login, upload, translation submission, status checks, and supported-language lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
