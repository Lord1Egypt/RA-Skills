## Description: <br>
A latest visitor data retrieval skill based on the Bee Website Builder Open API that obtains the latest visitor list and generates structured analysis data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxiaming](https://clawhub.ai/user/mouxiaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Website operators, analysts, and developers use this skill to retrieve recent Bee Website Builder visitor records, inspect traffic sources, and support visitor behavior analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return sensitive visitor analytics data, including IP addresses, URLs, referrers, user agents, and visit history. <br>
Mitigation: Use it only for authorized analytics work, limit retention and sharing of outputs, and handle returned data as sensitive personal or business data. <br>
Risk: The skill requires a Bee API key for access. <br>
Mitigation: Provide the key through the BEE_API_KEY environment variable or another secret manager, avoid pasting it into chat, and use least-privilege credentials. <br>


## Reference(s): <br>
- [Bee Website Builder Open API](https://open.tradew.com) <br>
- [Bee recent visitor API endpoint](https://platform.tradew.com/openapis/visitor/recent) <br>
- [ClawHub skill page](https://clawhub.ai/mouxiaming/bee-visitor-recent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mouxiaming) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis] <br>
**Output Format:** [JSON object with request status, pagination metadata, and visitor records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Visitor records can include IP addresses, URLs, referrers, user agents, visit timestamps, page data, and screen dimensions; page_size is limited to 10-50.] <br>

## Skill Version(s): <br>
2.0.3 (source: release evidence, skill.json, README.md, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
