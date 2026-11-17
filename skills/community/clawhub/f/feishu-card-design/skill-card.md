## Description:

Provides Chinese-first guidance, templates, and Python helpers for generating and validating Feishu/Lark Card 2.0 IM card JSON; it does not send messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to design, build, convert, and validate Feishu/Lark Card 2.0 notification payloads for reports, alerts, action lists, and status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cards may include links, callback payloads, or downstream OpenAPI sending code supplied by the caller.

Mitigation: Review and approve generated card links, callback payloads, and any actual Feishu/Lark message-sending code before deployment.

Risk: The scanner reported a validator reliability bug around malformed input handling.

Mitigation: Use the validator as a design-quality helper, not as a hardened security boundary, until malformed-input handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/feishu-card-design)
- [Project homepage](https://github.com/EdwardWason/feishu-card-design)
- [Feishu Card 2.0 component overview](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/card-components/overview)
- [Feishu card color enumerations](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/enumerations-for-fields-related-to-color)
- [Card 2.0 schema reference](references/card-2.0-schema.md)
- [Color system reference](references/color-system.md)
- [Title naming reference](references/title-naming.md)
- [Layout patterns reference](references/layout-patterns.md)
- [Compatibility reference](references/compatibility.md)
- [Accessibility reference](references/accessibility.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON Card 2.0 templates, examples, and Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Markdown or card JSON files and may write generated card JSON when the caller invokes the included scripts.]

## Skill Version(s):

1.0.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
