## Description: <br>
Bailian Ai Toolkit helps agents use the Bailian CLI to call Alibaba Cloud Bailian AI services for image, video, speech, vision, text, web search, and file upload tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocxf](https://clawhub.ai/user/cryptocxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate Bailian CLI commands and configuration guidance for Alibaba Cloud Bailian AI workflows, including media generation, speech processing, vision analysis, text chat, web search, and file upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file paths supplied to supported commands may be uploaded to Alibaba Cloud/Bailian services for processing. <br>
Mitigation: Treat local file paths as remote uploads and avoid confidential or regulated data unless approved for that service. <br>
Risk: The skill depends on a sensitive Bailian API key and an external bailian-cli package. <br>
Mitigation: Install the CLI only from a trusted source and use a dedicated, limited-scope API key where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cryptocxf/bailian-ai-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted bailian-cli installation and a configured Alibaba Cloud Bailian API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
