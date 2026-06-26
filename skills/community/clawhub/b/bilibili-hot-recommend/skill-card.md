## Description: <br>
无需登录状态下获取 bilibili（b站）首页热门推荐视频信息，包括视频名称、作者、视频地址、视频分类，获取热门视频排行榜 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvleiai123](https://clawhub.ai/user/lvleiai123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to retrieve current Bilibili popular-video recommendations without logging in. It helps summarize trending videos by title, creator, link, and category for trend monitoring or content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an undeclared third-party proxy domain to obtain Bilibili results. <br>
Mitigation: Install only when that proxy endpoint is acceptable for the deployment context, and review network access before use. <br>
Risk: The skill depends on the Python requests library. <br>
Mitigation: Confirm the runtime environment has requests installed and manage the dependency through the deployment's normal package controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvleiai123/bilibili-hot-recommend) <br>
- [Proxy endpoint used by skill](https://lvhomeproxy2.dpdns.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [Structured text list of video titles, creators, links, and categories] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the current popular-video list, with the skill documentation describing a default of the top 20 items.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
