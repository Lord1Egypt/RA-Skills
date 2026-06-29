## Description: <br>
抖音创作者中心评论管理助手。通过 Playwright 浏览器自动化抓取评论并批量回复，支持智能模板匹配和交互式可视化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Douyin creators, MCN teams, ecommerce operators, and social media staff use this skill to fetch unreplied comments, prepare template-based replies, execute approved replies, and generate HTML reports for comment operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs account-authorized browser automation that can post replies from the user's Douyin account. <br>
Mitigation: Run dry-run first, review the planned replies, keep conservative reply limits, and use the built-in delay controls before executing batch replies. <br>
Risk: Playwright profile data and output files may contain account session data or scraped user comments. <br>
Mitigation: Keep .playwright/douyin-profile and output files private, avoid sharing them, and remove them when no longer needed. <br>
Risk: Reply templates or generated replies may include content that conflicts with platform or account policies. <br>
Mitigation: Review reply templates and blocked keywords before use, avoid external links or sensitive contact prompts, and stop for manual handling when captcha or risk-control pages appear. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bettermen/douyin-comment-manager) <br>
- [Douyin API reference](references/douyin-api.md) <br>
- [Douyin Creator Center](https://creator.douyin.com/) <br>
- [Douyin comment reply API](https://open.douyin.com/video/comment/reply/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; workflow artifacts may include JSON data files and HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Playwright session data under .playwright/douyin-profile and comment or reply outputs under output/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
