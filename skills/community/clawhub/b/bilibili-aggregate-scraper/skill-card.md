## Description: <br>
Queries Bilibili video, creator, comment, danmaku, live, and search data through MaxHub APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and operations teams use this skill to collect and analyze Bilibili creator, video, comment, danmaku, live, and search data for creator evaluation, content analysis, and community research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Bilibili queries, identifiers, the MaxHub API key, and any user-provided session cookies to the third-party MaxHub service at aconfig.cn. <br>
Mitigation: Install only when the user trusts MaxHub with that data; avoid sharing session cookies when possible, and prefer scoped tokens or test accounts. <br>
Risk: VIP playback workflows may involve raw session cookies and account or content-access exposure. <br>
Mitigation: Use the VIP cookie playback endpoint only when the account risk is understood, then revoke or rotate cookies after use. <br>
Risk: The security summary notes unrelated Douyin and Xiaohongshu fallback paths that need review before broad deployment. <br>
Mitigation: Review and correct those fallback paths before deploying the skill widely. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/bilibili-aggregate-scraper) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Bilibili video API reference](references/api-video.md) <br>
- [Bilibili user API reference](references/api-user.md) <br>
- [Bilibili search API reference](references/api-search.md) <br>
- [Bilibili live API reference](references/api-live.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English responses; numeric formatting follows the user's detected language.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
