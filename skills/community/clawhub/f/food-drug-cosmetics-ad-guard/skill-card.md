## Description:

食药化妆品广告合规护栏。在药品 / 医疗器械 / 保健食品 / 特殊医学用途配方食品 / 化妆品 的广告文案、产品详情、直播话术、对外宣传发布前，实时拦截功效断言保证、治愈率有效率、疾病治疗宣称、处方药违规发布、医疗作用暗示、绝对化用语等 6 类高频违法违规表述，按风险分级给出整改建议。纯本地运行，零网络、零动态执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, compliance, legal, e-commerce, and agent workflow users can run this skill before publication to check Chinese food, drug, medical device, health food, special medical food, and cosmetics advertising copy for high-risk prohibited claims. It produces a local keyword-based risk decision with categories, severity, matched terms, and suggested revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a narrow local keyword guard for Chinese/PRC advertising compliance and is not legal advice or a complete approval workflow.

Mitigation: Use it as a pre-publication screening aid, then route flagged or final materials through qualified legal/compliance review and any required advertising approval process.

Risk: Keyword and substring matching can produce false positives, especially for negated or contextual statements.

Mitigation: Review each matched term in context before changing or blocking copy.

Risk: The guard does not verify administrative or technical status such as approval documents, advertiser qualifications, product registrations, or efficacy substantiation.

Mitigation: Pair this guard with a deeper checklist or audit workflow for licensing, registration, approval, and substantiation evidence before external release.

Risk: One CLI help label incorrectly mentions financial consumer protection.

Mitigation: Correct the help text before operational rollout so users understand the tool applies to food, drug, medical device, health food, special medical food, and cosmetics advertising compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/food-drug-cosmetics-ad-guard)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or structured JSON findings from a local CLI guard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs profile, risk level, decision, finding count, matched terms, categories, severities, spans, and revision suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json, CHANGELOG released 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
