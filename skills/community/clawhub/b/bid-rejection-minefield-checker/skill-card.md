## Description:

服务于投标人：输入单一省份、行业和采购方式后，基于历史否决案例库生成可打印的条款级雷区体检报告，包含当前文件定位、案例证据、风险等级和封标前自查表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and procurement teams use this skill before submission to scan a single project for province-scoped historical bid rejection risks, compare them with a current tender file or rejection record, and generate an audit-friendly Chinese report and checklist.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Reports are automatically branded with the maintainer signature and WeChat feedback footer.

Mitigation: Review or remove that footer before using reports in client-facing, legal, procurement, or white-label contexts.

Risk: Historical rejection reports may be mistaken for definitive legal or bid-decision advice.

Mitigation: Treat outputs as a pre-bid review aid and verify conclusions against the tender documents, governing rules, and qualified human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-rejection-minefield-checker)
- [README](artifact/README.md)
- [Knowledge Base Schema](artifact/references/kb-schema.md)
- [Test Cases](artifact/references/test-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown report with summary bullets, risk tables, source links, checklist items, and concise guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a single province, industry, and procurement method; an uploaded tender file or rejection record enables current-document comparison.]

## Skill Version(s):

1.0.0 (source: server release metadata, manifest.yaml, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
