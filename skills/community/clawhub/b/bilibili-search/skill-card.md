## Description: <br>
Searches Bilibili videos, retrieves video details and statistics, looks up creator information, and returns popular video and hot-search trend data without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Songrat](https://clawhub.ai/user/Songrat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to query Bilibili public data from an agent workflow, including video search, video statistics, creator profile summaries, popular videos, and hot-search trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to Bilibili public endpoints, so availability, response shape, and returned data can change outside the skill's control. <br>
Mitigation: Review outputs before relying on them and expect failures or changed fields when Bilibili updates public interfaces. <br>
Risk: High-frequency calls to public endpoints may trigger platform rate limits or anti-abuse controls. <br>
Mitigation: Keep request volume reasonable, avoid unnecessary repeated calls, and follow the artifact guidance to control call frequency. <br>
Risk: The security evidence notes a minor metadata transparency gap around network access. <br>
Mitigation: Install only when live requests to public trend and content platforms are acceptable for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Songrat/bilibili-search) <br>
- [Bilibili](https://www.bilibili.com) <br>
- [Bilibili search endpoint](https://api.bilibili.com/x/web-interface/search/type) <br>
- [Bilibili video detail endpoint](https://api.bilibili.com/x/web-interface/view) <br>
- [Bilibili hot-search endpoint](https://s.search.bilibili.com/main/hotword) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API Calls, Guidance] <br>
**Output Format:** [JSON returned by a Python command-line script, with Markdown usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by action and may include video URLs, titles, creators, engagement statistics, creator profile counts, popular video lists, or hot-search terms.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
