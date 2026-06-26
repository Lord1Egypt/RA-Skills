## Description: <br>
Retrieves 2026 Milan Winter Olympics medal standings, Team China medal details, live news, and schedules from Baidu Sports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Baidu Sports for Milan Winter Olympics medal rankings, news, event schedules, sport-specific schedules, and Team China medal information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js scripts that scrape Baidu Sports and uses randomized browser User-Agent values. <br>
Mitigation: Use only where this access pattern is acceptable; compliance-sensitive deployments should use transparent client identification, rate limits, and confirmation that source-site access is allowed. <br>
Risk: Baidu Sports data is fetched live and may be delayed, unavailable, or changed by the source site. <br>
Mitigation: Treat returned scores, schedules, and news as source-dependent data and verify high-impact results against an authoritative event source before publication or operational use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wuchubuzai2018/baidu-milan-winter-olympics-2026) <br>
- [Baidu Sports](https://tiyu.baidu.com/) <br>
- [Baidu Sports Milan Winter Olympics Medal Standings](https://tiyu.baidu.com/al/major/home?match=2026%E5%B9%B4%E7%B1%B3%E5%85%B0%E5%86%AC%E5%A5%A5%E4%BC%9A&tab=%E5%A5%96%E7%89%8C%E6%A6%9C) <br>
- [Baidu Sports Milan Winter Olympics News](https://tiyu.baidu.com/al/major/home?match=2026%E5%B9%B4%E7%B1%B3%E5%85%B0%E5%86%AC%E5%A5%A5%E4%BC%9A&tab=%E7%9B%B4%E5%87%BB%E7%8E%B0%E5%9C%BA) <br>
- [Baidu Sports Milan Winter Olympics Schedule API](https://tiyu.baidu.com/al/major/schedule/list) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with Node.js command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Baidu Sports URLs, medal counts, event metadata, news metadata, schedule status, and video or image links when returned by the source site.] <br>

## Skill Version(s): <br>
0.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
