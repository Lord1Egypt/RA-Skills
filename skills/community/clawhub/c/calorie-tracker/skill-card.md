## Description: <br>
Smart health management solution with food and exercise recognition, nutrition and calorie analysis, secure data storage, and comprehensive data management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guangxiankeji](https://clawhub.ai/user/guangxiankeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log and query food, exercise, and weight records, estimate nutrition and calorie expenditure, and review health-tracking summaries. Agents may call provider APIs to analyze entries and persist confirmed records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive food, exercise, weight, image, email, and token data through provider services while privacy, token, and regional boundaries are unclear. <br>
Mitigation: Use only with a trusted provider account; confirm data storage location, token protection and revocation, and retention practices before deployment. <br>
Risk: The release carries purchase, crypto, OAuth-token, and sensitive-credential capability tags that are not fully explained by the calorie-tracking workflow. <br>
Mitigation: Review the requested capabilities before installation and disable or reject deployment if those capabilities are not required for the intended use. <br>
Risk: The artifact behavior stores health records in cloud services after user confirmation and uses Bearer-token authentication. <br>
Mitigation: Require explicit user consent for storage, avoid exposing access tokens in prompts or logs, and rotate or revoke tokens if access is no longer needed. <br>


## Reference(s): <br>
- [Calorie Tracker ClawHub page](https://clawhub.ai/guangxiankeji/calorie-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/guangxiankeji) <br>
- [Calorie Tracker homepage](https://us.guangxiankeji.com/calorie/) <br>
- [US API specification](https://us.guangxiankeji.com/calorie/service/user/api-spec) <br>
- [China API specification](https://cn.guangxiankeji.com/calorie/service/user/api-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Concise natural-language responses with structured nutrition, exercise, weight, and record-management summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request user confirmation before storing health records and may require email verification plus Bearer-token authentication for API-backed storage and queries.] <br>

## Skill Version(s): <br>
1.0.24 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
