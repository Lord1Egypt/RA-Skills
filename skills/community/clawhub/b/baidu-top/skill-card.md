## Description: <br>
获取百度首页热搜、小说、电影、电视剧等榜单。当用户说：百度今天热搜榜？热播剧榜单，或类似百度榜单问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current Baidu homepage ranking lists for hot searches, novels, movies, and TV dramas, then return either readable grouped text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to Baidu ranking pages and depends on Baidu page availability and structure. <br>
Mitigation: Use it only when live Baidu ranking data is needed, expect occasional fetch or parsing failures, and review results before relying on them. <br>
Risk: The skill may require Python dependencies that are not already installed. <br>
Mitigation: Install the documented Python packages in the execution environment before running the script. <br>
Risk: High request frequency may trigger Baidu rate limits or other access controls. <br>
Mitigation: Run requests at a reasonable frequency and adjust timeout or User-Agent only when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/baidu-top) <br>
- [Baidu Top Source Page](https://top.baidu.com/board?platform=pc&tab=homepage&sa=pc_index_homepage_all) <br>
- [JisuAPI Publisher Site](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Readable grouped text by default, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live Baidu page fetch with configurable limit, timeout, and User-Agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
