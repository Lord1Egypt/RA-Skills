## Description:

协助用户通过 CQCCJY 公共用户端选择知网论文检测产品、上传论文、查询订单、获取报告并前往官方入口验真。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and authors use this skill to choose an appropriate CNKI paper or AIGC check, submit a selected paper through CQCCJY, track the order, and interpret or verify the resulting report. Users complete payment and verification themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected paper is uploaded to an external checking service and may contain sensitive unpublished work.

Mitigation: Confirm the intended file and service with the user before upload, and use only the documented HTTPS public portal.

Risk: Payments, card settlement, and verification can expose credentials or lead to unintended charges if delegated.

Mitigation: Have the user complete payment, card settlement, and CAPTCHA in the browser; never request passwords or unrelated credentials.

Risk: A personal precheck or successful report verification may be mistaken for an institution's acceptance decision.

Mitigation: Defer to the school or journal's written requirements and distinguish report authenticity from passing their criteria.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zslzxy/skills/cnki-paper-check)
- [CQCCJY public paper-check portal](https://cnki.cqccjy.cn/pzw)
- [CNKI report verification](https://check7.cnki.net/codeverify/)
- [Public workflow reference](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides product guidance, order status, report handoff, and verification instructions; does not perform payment or CAPTCHA entry.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
