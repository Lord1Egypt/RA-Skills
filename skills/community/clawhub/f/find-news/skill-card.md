## Description: <br>
查找资料 provides multi-engine web, news, social, video, and code search through a cloud Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LazyBoyJgn99](https://clawhub.ai/user/LazyBoyJgn99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs current web or news results from engines such as Google, Baidu, Bing, DuckDuckGo, Yahoo, WeChat, YouTube, GitHub, Reddit, or Bilibili. It can return fast result summaries by default and optionally request full page content when explicitly needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a shared API key and sends user searches to an unclear HTTP endpoint. <br>
Mitigation: Use only non-sensitive searches unless the publisher replaces the embedded key with a user-managed credential, provides HTTPS on a clearly owned endpoint, and documents privacy, retention, caching, and cost controls. <br>
Risk: Full-content crawling can significantly increase latency and cost. <br>
Mitigation: Keep crawl_results at 0 by default, limit max_results, and request full content only when the user explicitly needs it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LazyBoyJgn99/find-news) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON search or news results with agent-facing request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search summaries are the default; full content is requested only when crawl_results is greater than 0.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
