## Description: <br>
内容捕手 Content Hunter scrapes trending short-video content from Xiaohongshu, Douyin, and Bilibili, then saves platform data and generates scheduled reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[judefluen-coder](https://clawhub.ai/user/judefluen-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users use this skill to collect trending social video content across Xiaohongshu, Douyin, and Bilibili, archive per-platform Markdown data, and produce daily or scheduled trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use logged-in browser sessions and persist scraped social-platform content. <br>
Mitigation: Run it only with accounts and platforms you are authorized to access, review stored archives, and delete retained data when it is no longer needed. <br>
Risk: The skill supports recurring scraping jobs and report delivery to a fixed group destination. <br>
Mitigation: Review scheduled jobs and the destination before enabling automation, and disable or remove related cron jobs after the reporting workflow is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/judefluen-coder/content-hunter) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [Douyin](https://www.douyin.com) <br>
- [Bilibili](https://www.bilibili.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown data files, Markdown summary reports, and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped task folders and can aggregate multiple platform captures into a report.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
