## Description: <br>
V002 fetches public hot-list data from Bilibili, Douyin, and Toutiao and can summarize the retrieved trend items for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loveyou001](https://clawhub.ai/user/loveyou001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current public trend lists from supported Chinese media platforms and optionally generate a short text or JSON summary for content monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Bilibili, Douyin, and Toutiao endpoints during normal use. <br>
Mitigation: Run it only in environments where this outbound network access is acceptable and review egress policies before deployment. <br>
Risk: Documentation claims AI summaries, push delivery, scheduling, and additional platform coverage that are not supported by the scanned code. <br>
Mitigation: Treat those claims as marketing or future work and rely on the code-supported Bilibili, Douyin, and Toutiao behavior unless additional implementation is added. <br>
Risk: Embedded metadata and registry metadata do not fully align. <br>
Mitigation: Verify the package identity, publisher handle, and release version before installing or distributing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loveyou001/databass001) <br>
- [Bilibili popular endpoint](https://api.bilibili.com/x/web-interface/popular) <br>
- [Douyin hot search endpoint](https://www.douyin.com/aweme/v1/web/hot/search/list/) <br>
- [Toutiao hot board endpoint](https://www.toutiao.com/hot-event/hot-board/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text with optional JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and outbound access to supported public platform endpoints.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact files also contain 4.0.1, 1.0.0, and 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
