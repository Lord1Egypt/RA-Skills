## Description: <br>
Datayes Web Search uses the Datayes gptMaterials/v2 API to run structured semantic searches across news, research reports, announcements, meeting summaries, and indicator background materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datayes](https://clawhub.ai/user/datayes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users who need current Datayes-indexed financial or industry materials use this skill to query news, research reports, announcements, meeting summaries, and indicators through a Python helper with a Datayes token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Datayes skill page](https://clawhub.ai/datayes/datayes-web-search) <br>
- [Datayes token login](https://r.datayes.com/auth/login) <br>
- [Datayes gptMaterials/v2 API endpoint](https://gw.datayes.com/aladdin_info/web/gptMaterials/v2) <br>
- [Datayes API metadata endpoint](https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output is raw JSON arrays.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and DATAYES_TOKEN. The skill sends queries and the token to Datayes endpoints and prints raw API JSON results, so avoid sensitive query terms or returned data in untrusted chats or logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
