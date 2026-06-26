## Description: <br>
Анализ рекламных кампаний Яндекс.Директ <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimblemarketingapex-netizen](https://clawhub.ai/user/nimblemarketingapex-netizen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing teams and advertising analysts use this skill to review Yandex Direct campaign performance, including CTR, CPC, spend, conversions, weak ads, and keyword opportunities. It returns concise optimization recommendations for bids, budgets, ad text, calls to action, and audience segments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses advertising-account credentials to access Yandex Direct statistics. <br>
Mitigation: Use a least-privilege token and confirm the CLIENT_LOGIN account before running analysis. <br>
Risk: Broad trigger words can cause the skill to run during general advertising discussions. <br>
Mitigation: Confirm that the user intends to analyze Yandex Direct campaign data before accessing account statistics. <br>
Risk: Recommendations about bids, budgets, campaigns, or ads could affect paid advertising performance if applied automatically. <br>
Mitigation: Require explicit approval before any campaign, bid, budget, or ad change. <br>


## Reference(s): <br>
- [Direct Analysis on ClawHub](https://clawhub.ai/nimblemarketingapex-netizen/direct-analysis) <br>
- [Publisher profile: nimblemarketingapex-netizen](https://clawhub.ai/user/nimblemarketingapex-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise analysis and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and Yandex Direct credentials supplied through the agent environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
