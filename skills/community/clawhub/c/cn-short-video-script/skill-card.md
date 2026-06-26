## Description: <br>
Generates Chinese short-video scripts for platforms such as Douyin, Xiaohongshu, and WeChat Channels, including hooks, shot-by-shot scenes, dialogue, sound cues, and filming suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and agent users use this skill to draft Chinese short-video scripts from a topic, product, target platform, and script style. It can produce local template-based output or optionally use an OpenAI API key for AI-assisted generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional AI mode can send the topic and generation prompt to OpenAI when OPENAI_API_KEY is set. <br>
Mitigation: Unset OPENAI_API_KEY or avoid the AI mode when fully local template output is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freedompixels/cn-short-video-script) <br>
- [Publisher Profile](https://clawhub.ai/user/freedompixels) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Chinese plain text or Markdown-style script sections with shot descriptions, dialogue, sound cues, timing, and filming tips] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional OpenAI-powered mode may call OpenAI when OPENAI_API_KEY is set; otherwise the helper falls back to local templates.] <br>

## Skill Version(s): <br>
1.2.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
