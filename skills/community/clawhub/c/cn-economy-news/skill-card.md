## Description: <br>
获取中国经济资讯，仅从官方权威媒体抓取高质量经济新闻并过滤广告和低质量内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gchenxx](https://clawhub.ai/user/Gchenxx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve current Chinese economic news from listed official media sources, filter low-quality or promotional results, and summarize selected articles when deeper reading is requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback news fetching may run local Python code, require dependencies, and query external public websites. <br>
Mitigation: Review the script before execution, install dependencies from trusted package sources, and run it in an environment appropriate for public web requests. <br>
Risk: The source feed may not be a perfectly guaranteed official-only feed because hostname validation and TLS handling have caveats. <br>
Mitigation: Verify article hostnames and links before relying on results for high-stakes decisions. <br>
Risk: Economic news results are time-sensitive and can become stale. <br>
Mitigation: Check the update timestamp and refresh results before using them in current reporting or analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gchenxx/cn-economy-news) <br>
- [中国政府网政策 RSS](https://www.gov.cn/zhengce/zuixin/ezine.xml) <br>
- [新华网财经频道](http://www.news.cn/fortune/) <br>
- [人民网财经频道](http://finance.people.com.cn/) <br>
- [中国经济网](https://www.ce.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown news lists or JSON article objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article titles, links, source groupings, update timestamps, and concise summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
