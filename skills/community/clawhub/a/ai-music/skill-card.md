## Description: <br>
Ai Music helps users generate AI-created songs or instrumental tracks with MakeBestMusic and check generation status from returned music IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sthk-mbm](https://clawhub.ai/user/sthk-mbm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and musicians use this skill to turn song descriptions into generated music, choose vocals or instrumental output, and check whether generated tracks are ready. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MakeBestMusic API key and sends song generation requests to that service. <br>
Mitigation: Use a dedicated key where possible, store it only in the skill configuration, and rotate or revoke it if exposed. <br>
Risk: Song descriptions and generated music IDs are shared with MakeBestMusic. <br>
Mitigation: Avoid including sensitive personal information or confidential material in music prompts. <br>
Risk: Music generation is asynchronous and may remain pending or fail. <br>
Mitigation: Check returned music IDs before presenting completion, and retry with a simpler description if generation fails. <br>


## Reference(s): <br>
- [ClawHub Ai Music release page](https://clawhub.ai/sthk-mbm/ai-music) <br>
- [MakeBestMusic account and API key page](https://makebestmusic.com/?pid=PIDcLjhgCXUQ) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON generation or status results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MakeBestMusic apiKey; generated music links are returned after asynchronous status checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
