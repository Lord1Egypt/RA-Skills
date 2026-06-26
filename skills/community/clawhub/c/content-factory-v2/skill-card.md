## Description: <br>
Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with user, writing professional content through self-iteration, and outputting both Markdown and HTML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and agent users use this skill to research a topic, develop WeChat article angles, draft long-form Chinese content, generate formatted Markdown and HTML, and optionally prepare cover images or WeChat draft submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access WeChat publishing credentials and create WeChat drafts or previews. <br>
Mitigation: Install only when that publishing access is intended, keep credentials out of chat output and logs, and require manual review before any draft or preview submission. <br>
Risk: Credential-looking values or .env contents may be exposed if diagnostic commands are run carelessly. <br>
Mitigation: Remove or rotate any exposed secrets, avoid commands that print API keys or dump .env files, and use environment variables or protected .env files with least-privilege credentials. <br>
Risk: The workflow can use a WeChat proxy for publishing actions. <br>
Mitigation: Use only a trusted HTTPS proxy that the publisher controls and verify the destination before sending WeChat API credentials or article content. <br>
Risk: Generated article claims or viral-style framing may be inaccurate or misleading without source review. <br>
Mitigation: Review citations, dates, and statistics against the gathered sources before publishing the generated Markdown or HTML. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeffli2002/content-factory-v2) <br>
- [YouTube Research Checklist](references/youtube_research_checklist.md) <br>
- [WeChat Viral Content Frameworks](references/wechat_viral_frameworks.md) <br>
- [WeChat Formatting Rules](references/wechat-format-rules.md) <br>
- [WeChat Publish Rules](references/WECHAT_PUBLISH_RULES.md) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [API Key Setup Guide](API_KEY_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and HTML article drafts with optional shell commands, configuration guidance, and publishing workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeChat-ready HTML, cover-image generation commands, and draft publishing steps that require human review before submission.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
