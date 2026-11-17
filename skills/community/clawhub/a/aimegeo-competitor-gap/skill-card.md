## Description:

比较品牌与竞品的同类页面，输出有证据的 GEO 内容差距与三项行动建议；没有真实回答样本时不推断 AI 排名。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

营销与内容团队可用它比较指定的品牌和竞品页面，识别 FAQ、品牌实体、来源资料、结构数据与抓取信号的差距，并据此安排内容改进。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can contain private inputs, and the optional aimeGeo integration can publish content to external accounts.

Mitigation: Use only authorized files and trusted public URLs, protect reports containing private inputs, review the integration, and approve final content and target accounts before publishing.

## Reference(s):

- [比较方法](references/methodology.md)
- [输入与输出格式](references/input-output.md)
- [RFC 9309：Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html#section-2.2.2)
- [Google robots.txt 规则](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec#order-of-precedence-for-rules)
- [aimeGeo integration](https://github.com/aiispower/aimegeo)

## Skill Output:

**Output Type(s):** [Analysis, CSV, Markdown, JSON]

**Output Format:** [CSV gap matrix, Markdown recommendations, and JSON evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusions are scoped to supplied pages; AI citation or ranking claims require real answer and native citation samples.]

## Skill Version(s):

1.0.1 (source: server release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
