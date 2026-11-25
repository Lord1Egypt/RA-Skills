## Description:

当用户准备直播带货，需要整场流程、商品讲解、互动问答和转场话术时使用。根据排品清单、真实商品资料与已确认活动规则，输出可照读的话术和时间表。已有资料可直接写；抖音、小红书商品详情可按需补充。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and live stream hosts use this skill to prepare a timed live-selling run of show, read-aloud product scripts, audience Q&A, transitions, and closing remarks based on supplied product facts and confirmed promotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious because it runs the socialdatax-skills CLI at mutable latest, creating supply-chain risk for credentials and process permissions.

Mitigation: Review and pin the CLI version before use, and run it only where credentials and process permissions are limited to what the task needs.

Risk: The security scan was partial because two local references were unresolved, so its evidence is incomplete.

Mitigation: Resolve the missing references and review the relevant files before relying on the scan assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/ecommerce-live-sales-script)
- [SocialDataX](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a timed run-of-show, read-aloud product scripts, Q&A, transitions, and closing remarks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied product facts and confirmed promotion terms; missing facts and seller verification items are called out separately.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
