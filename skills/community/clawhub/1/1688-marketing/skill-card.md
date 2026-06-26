## Description: <br>
Helps 1688 merchants query marketing enrollment activities, check suggested offer prices, submit confirmed activity enrollments, and review opportunity recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 merchants and their agents use this skill to discover marketing activities and market opportunities, check suggested offer prices, and submit enrollment requests after merchant confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a 1688 merchant AK and may handle OAuth tokens. <br>
Mitigation: Use the skill only in a trusted workspace, avoid pasting AKs into chat or logs, and clear stored credentials when finished. <br>
Risk: The skill can submit 1688 marketing enrollments that affect merchant activity participation. <br>
Mitigation: Run enrollment submission only after the merchant has reviewed the suggested price and explicitly confirmed the action. <br>
Risk: The temporary authorization callback server and token fallback are broader than the documentation suggests. <br>
Mitigation: Complete authorization only in a trusted local environment and review stored credentials or callback behavior before broad deployment. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/1688aiinfra/1688-marketing) <br>
- [1688 AK Portal](https://clawhub.1688.com/) <br>
- [1688招商活动查询指南](references/capabilities/1688_enroll_activity_query.md) <br>
- [1688招商活动商品信息及建议价查询指南](references/capabilities/1688_enroll_offer_query.md) <br>
- [1688招商活动报名指南](references/capabilities/1688_enroll_submit_item.md) <br>
- [商机推荐查询指南](references/capabilities/1688_opp_recommend.md) <br>
- [AK 配置指南](references/capabilities/configure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with optional Markdown summaries and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call 1688 APIs and require an AK or OAuth token; enrollment submission writes marketing data only after confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
