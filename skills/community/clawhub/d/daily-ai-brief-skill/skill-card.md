## Description: <br>
一个简洁高效的AI新闻简报生成技能。每日自动从多个可靠数据源采集AI领域最新动态，生成干净的Markdown格式简报，帮助您快速掌握AI行业前沿信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanll](https://clawhub.ai/user/yanll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to collect recent AI news from configured RSS feeds, APIs, websites, and X/Twitter accounts, then generate structured daily briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts many external websites, feeds, APIs, and social platforms while collecting briefing content. <br>
Mitigation: Review and limit src/data_sources.yaml before running the skill, especially in restricted network or compliance environments. <br>
Risk: The skill uses browser automation and scraping behavior that may create privacy, reliability, or terms-of-service concerns. <br>
Mitigation: Run it in a sandboxed environment where possible and disable sources or scrapers that are not appropriate for the user's policy requirements. <br>
Risk: Collected third-party content is saved locally in generated reports. <br>
Mitigation: Handle generated reports as externally sourced content and review them before sharing or using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanll/daily-ai-brief-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yanll) <br>
- [README](artifact/README.md) <br>
- [Data source configuration](artifact/src/data_sources.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, configuration] <br>
**Output Format:** [Markdown and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written to a local reports directory and include source links for collected items.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
