## Description:

获取中国经济资讯。仅从官方权威媒体（中国政府网、新华网、人民网、国家统计局、央视财经、中国经济网）抓取高质量经济新闻，自动过滤广告和低质量内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchenxx](https://clawhub.ai/user/gchenxx)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to gather timely Chinese economic policy, macroeconomic, and finance news from the official sources named by the skill. It can return grouped news links, keyword-filtered results, JSON output from the fallback script, and brief article takeaways when a user requests deeper reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback script can present unauthenticated or spoofed links as official news.

Mitigation: Treat generated links as unverified unless the script is fixed to require HTTPS, validate certificates, and check parsed hostnames against an exact allowlist.

Risk: The skill depends on web access to Chinese news sites and Bing, so availability and freshness can vary.

Mitigation: Review results before relying on them and clearly communicate the timestamp or freshness of returned news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gchenxx/skills/cn-economy-news)
- [中国政府网政策 RSS](https://www.gov.cn/zhengce/zuixin/ezine.xml)
- [新华网财经频道](http://www.news.cn/fortune/)
- [人民网财经频道](http://finance.people.com.cn/)
- [中国经济网](https://www.ce.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown grouped by news source, JSON article lists, or concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include article titles, links, dates, source names, categories, and update timestamps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
