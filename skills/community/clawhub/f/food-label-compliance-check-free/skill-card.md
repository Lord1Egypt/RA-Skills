## Description:

食品标签与配料表台账逐项核对（配料表顺序、配料与投料记录一致性、致敏物质提示、营养成分表算术与 NRV% 复算、批次重复与同日两个标签版本、字段合法性），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Food production quality, R&D, label, and food-safety staff use this skill before new product launches or packaging revisions to check Chinese food-label and ingredient-ledger consistency. It performs six narrow table checks and cites source lines for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the output as a full legal compliance determination.

Mitigation: Present results as narrow consistency checks and require qualified review for regulatory decisions.

Risk: Important label issues may be missed because PDFs, images, label layout, supplier evidence, and full regulatory validity are outside scope.

Mitigation: Use the skill alongside source-document review, supplier evidence checks, and applicable food-label regulatory review.

Risk: Incomplete or malformed input can lead to misleading confidence if interpreted as a pass.

Mitigation: Preserve the insufficient-input behavior: list missing fields and do not issue a compliance conclusion when required data is absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/food-label-compliance-check-free)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Human-readable text or JSON containing check status, missing-input guidance, executed check list, and line-cited findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful checks cite source lines; insufficient input returns missing fields and does not produce a compliance conclusion.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
