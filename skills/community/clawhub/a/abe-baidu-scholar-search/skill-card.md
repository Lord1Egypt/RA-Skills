## Description: <br>
Academic Literature Search Tool enables the retrieval of both Chinese and English literature, covering various types of literature such as academic journals, conference papers, and dissertations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developer agents use this skill to submit academic literature search queries and retrieve structured Chinese and English results from the SkillBoss API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords and the SKILLBOSS_API_KEY are sent to the SkillBoss/HeyBoss API endpoint. <br>
Mitigation: Use the skill only when third-party processing is acceptable, and avoid confidential project names, unpublished research topics, personal data, or secrets in search queries. <br>
Risk: The skill depends on a valid sensitive API credential in the runtime environment. <br>
Mitigation: Store SKILLBOSS_API_KEY securely, limit access to the runtime environment, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Baidu Scholar](https://xueshu.baidu.com/) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-baidu-scholar-search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON API responses with Markdown usage guidance and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SKILLBOSS_API_KEY; sends search keywords to the SkillBoss/HeyBoss API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
