## Description: <br>
AI 视频剪辑器 helps agents send selected MP4 videos to Sparki, create AI editing jobs from style tips and natural-language prompts, and return a temporary download link for the edited result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to automate short-form video editing, highlight extraction, captions or commentary, aspect-ratio conversion, vlogs, montages, and talking-head clips from MP4 source footage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected MP4 files, prompts, and style settings are sent to Sparki for remote processing. <br>
Mitigation: Use only footage approved for that transfer, and avoid confidential, regulated, copyrighted, or non-consented material unless your organization has approved the workflow. <br>
Risk: The skill requires SPARKI_API_KEY and returns temporary result links that may provide access to processed videos. <br>
Mitigation: Keep the API key private, avoid logging or sharing it, and treat returned download links as sensitive until they expire. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/ai-video-editor-zh) <br>
- [Sparki](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and plain-text result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPARKI_API_KEY, curl, and jq; accepts MP4 input up to 3 GB; result links are temporary.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
