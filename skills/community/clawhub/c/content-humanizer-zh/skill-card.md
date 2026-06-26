## Description: <br>
将 AI 生成的内容转化为自然的人类写作风格，支持润色文章、帖子和邮件，去除常见 AI 写作痕迹，并按 InStreet、小红书、公众号和知乎等平台调整语气。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyhw](https://clawhub.ai/user/wyhw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, marketers, community managers, and agent users use this skill to rewrite Chinese AI-generated text so it reads more naturally while preserving the original meaning. It can also score text quality and adapt output for supported publishing platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewritten text could imply unaided human authorship, firsthand experience, or personal claims that are not true. <br>
Mitigation: Review the rewritten text before publishing and remove or qualify claims that the author cannot support. <br>
Risk: Local text passed to the Python helper may contain sensitive or unpublished material. <br>
Mitigation: Run the helper only with text the user intends to transform and is allowed to process locally. <br>


## Reference(s): <br>
- [AI writing patterns](references/ai-patterns.md) <br>
- [Platform style guide](references/platform-styles.md) <br>
- [ClawHub skill page](https://clawhub.ai/wyhw/content-humanizer-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional command examples and score output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include rewritten Chinese text, platform-specific style adjustments, and an optional 50-point quality score.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
