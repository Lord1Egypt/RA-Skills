## Description: <br>
易企秀是创意营销平台，提供个人简历、翻页 H5 邀请函、营销海报、长页 H5、表单问卷、微信互动游戏、视频等海量模板；本 Skill 用于搜索易企秀商城模版资源，并返回标题、链接、描述、浏览量等结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijun](https://clawhub.ai/user/jijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search the Eqxiu marketplace for H5 templates, invitations, forms, long pages, e-books, and other marketing assets. The agent runs the search with keyword and optional filter parameters, then presents result titles, preview links, descriptions, and page views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to Eqxiu's marketplace search service. <br>
Mitigation: Avoid private or sensitive terms as search keywords, especially in restricted environments. <br>
Risk: Broad trigger phrases such as 表单 or 长页 may activate the skill for generic template-search requests. <br>
Mitigation: Narrow the trigger phrases when generic Chinese template terms are common in the deployment environment. <br>
Risk: Search results depend on Eqxiu service behavior and may be incomplete or stale if the site changes. <br>
Mitigation: Review returned links before using them and adjust keywords or filters when results do not match the user's intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jijun/eqxiu-store-skill) <br>
- [Eqxiu](https://www.eqxiu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON arrays from the search script, summarized as Markdown or plain text by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include title, preview link, description, and page views; optional filters include price range, color, page number, sort order, and page size.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
