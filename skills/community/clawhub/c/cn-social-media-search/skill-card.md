## Description: <br>
社交媒体搜索技能。支持抖音,小红书,b站搜索。当用户提到 /搜索抖音 或 /搜索小红书 或 /B站搜索 时，自动打开对应网站并搜索指定内容，返回搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiao4d-lyf](https://clawhub.ai/user/xiao4d-lyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Douyin, Xiaohongshu, and Bilibili for a provided query and summarize returned social media results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may reflect signed-in, personalized, or account-visible content. <br>
Mitigation: Sign out or use a separate browser profile before running searches when personalized results are not desired. <br>
Risk: Slash-style triggers can cause accidental browsing if invoked unintentionally. <br>
Mitigation: Use explicit search commands and confirm the target platform and query before navigating. <br>
Risk: Hard-coded page references for Douyin and Xiaohongshu may become stale as the sites change. <br>
Mitigation: If a search fails, inspect a fresh browser snapshot and update the page reference before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiao4d-lyf/cn-social-media-search) <br>
- [Douyin](https://www.douyin.com) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Bilibili search](https://search.bilibili.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown search summaries with OpenClaw browser command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned snapshots may reflect account-visible or personalized content from the target sites.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and SKILL.md version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
