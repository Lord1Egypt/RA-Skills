## Description:

稻哲纪烤羊排智能客服Skill。当用户询问关于稻哲纪烤羊排的任何信息时触发：包括营业时间、门店地址、招牌菜推荐、菜品介绍、价格、外卖配送、团购套餐、会员福利、停车、Wi-Fi等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT

## Use Case:

External customers use this skill to get restaurant customer-service answers for 稻哲纪烤羊排, including store information, menu recommendations, prices, delivery, promotions, membership benefits, reservations, and common dining questions. The agent is expected to read the bundled reference files before answering business-specific facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installers add unattended daily self-updates that may pull future changes without review.

Mitigation: Prefer manual installation from a reviewed, version-pinned archive and remove or skip the cron or scheduled-task updater.

Risk: Installers can overwrite an existing local daozheji-grill skill directory.

Mitigation: Back up any existing skill directory before installation and review file changes before replacing local content.

Risk: Customer answers about allergens or food safety can be misleading if the agent responds from memory.

Mitigation: Require the agent to read the bundled FAQ and service reference files for food-safety and allergen questions, and direct customers with allergy symptoms to medical professionals.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/liubuq-sys/skills/daozheji-grill)
- [Brand information](references/brand.md)
- [Business information](references/business-info.md)
- [FAQ](references/faq.md)
- [Promotions](references/promotions.md)
- [Services](references/services.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Natural-language customer-service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in the bundled reference files for current business details.]

## Skill Version(s):

1.0.0 (source: release metadata, version.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
