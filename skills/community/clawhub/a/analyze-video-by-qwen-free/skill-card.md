## Description: <br>
Analyze Video By Qwen Free helps agents analyze local video files with Qwen 3.5 Plus through Alibaba Cloud DashScope and return basic scene descriptions and content summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creators use this skill to submit local video files for quick scene description and basic content understanding through DashScope, using default frame sampling and prompt settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends local video content to Alibaba Cloud DashScope for remote analysis. <br>
Mitigation: Use it only with media approved for external processing, and avoid sensitive or regulated videos unless an appropriate approval path is in place. <br>
Risk: The documented API key check command may expose credentials in terminal output or logs. <br>
Mitigation: Configure credentials carefully and avoid commands or logging practices that print API keys. <br>
Risk: The trigger language is broader than the actual video-analysis behavior. <br>
Mitigation: Use the skill specifically for local video content analysis and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/analyze-video-by-qwen-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-shaped analysis output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses default FPS=2 and a default prompt; outputs a basic scene/content summary or error guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
