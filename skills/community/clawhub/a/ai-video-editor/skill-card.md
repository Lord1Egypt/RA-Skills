## Description: <br>
Raw assets and requirements in, result video out: edit any type of video with Sparki, the video agent powered by Gemini multimodal AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolk](https://clawhub.ai/user/symbolk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload local MP4 assets, provide editing requirements, create a Sparki render project, poll for completion, and download the final MP4 result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected MP4 files are uploaded to Sparki's remote service for processing. <br>
Mitigation: Use the skill only with videos the user is authorized to share externally and confirm the upload before execution. <br>
Risk: The security review notes that manifest declarations could be more explicit about network, file, environment, and execution needs. <br>
Mitigation: Review the declared runtime needs before installation and restrict execution to environments where SPARKI_API_KEY and selected video files are appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/symbolk/ai-video-editor) <br>
- [Publisher Profile](https://clawhub.ai/user/symbolk) <br>
- [Sparki Homepage](https://sparki.io) <br>
- [Sparki Business API Base URL](https://business-agent-api.sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPARKI_API_KEY and a local MP4 input; uploads selected MP4 files to Sparki's remote service for processing.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
