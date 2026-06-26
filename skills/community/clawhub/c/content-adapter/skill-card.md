## Description: <br>
Content Adapter transforms a source text or Markdown draft into platform-specific versions for Xiaohongshu, WeChat Official Account, Zhihu, Weibo, Douyin, Bilibili, and Toutiao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeliang2000](https://clawhub.ai/user/mikeliang2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and publishing teams use this skill to rewrite one source draft into channel-specific copy with adjusted length, tone, formatting, emoji use, hashtags, and calls to action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buried analytics instructions describe automatic reporting of skill use, completion, errors, sharing, user IDs, and output characteristics without clear consent or scope. <br>
Mitigation: Verify whether the runtime provides analytics-sdk or trackEvent, remove or ignore the analytics template if telemetry is not desired, and disclose any remaining telemetry before use. <br>
Risk: Publisher and author signals differ across server metadata, skill frontmatter, and the install script. <br>
Mitigation: Treat the server-resolved publisher handle as the owner for this card and confirm publisher identity before deployment. <br>
Risk: Generated platform copy can create copyright, policy, or moderation issues if used to rewrite unlicensed or sensitive content. <br>
Mitigation: Use only content the operator has rights to adapt, review generated drafts against each target platform's rules, and manually check sensitive topics before publishing. <br>


## Reference(s): <br>
- [Content Adapter ClawHub listing](https://clawhub.ai/mikeliang2000/content-adapter) <br>
- [Publisher profile](https://clawhub.ai/user/mikeliang2000) <br>
- [Publisher homepage](https://hermesai.ltd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text platform-specific drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific headings, emoji, hashtags, calls to action, and formatting suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
