## Description:

为一审败诉后的民事上诉整理判决推理、证据差异、请求权路径、事实台账和配套文书草稿，并要求逐条标注出处及递交前核验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

自行处理或协助整理民事二审的当事人，可用它拆解一审判决、逐项比对证据、建立有出处的事实台账，并准备上诉草稿与递交待办。它提供结构化工作流，不提供法律意见，也不替代律师。

### Deployment Geography for Use:

China (Chinese civil appeal procedure)

## Known Risks and Mitigations:

Risk: Optional online diagnostics could expose CUE_API_KEY to an unapproved destination.

Mitigation: Prefer the local workflow without a key; before online use, independently verify HTTPS and approve the destination for that credential.

Risk: External parsing may send confidential case materials to a provider.

Mitigation: Approve each file before external parsing and review the provider's confidentiality and retention terms.

Risk: Word export can change numbering or cross-references even when the text coverage check passes.

Mitigation: Manually compare Word numbering and cross-references with the source document before filing.

## Reference(s):

- [判决逆向工程](artifact/references/01-judgment-reverse-engineering.md)
- [证据逐字比对协议](artifact/references/02-evidence-diff-protocol.md)
- [请求权路径阶梯](artifact/references/03-legal-ladder.md)
- [事实台账与纪律](artifact/references/04-fact-ledger-and-discipline.md)
- [自行诉讼与递交流程](artifact/references/05-self-represented-filing.md)
- [文书包与 Word 导出](artifact/references/06-document-pack.md)
- [脱敏实例](artifact/references/07-worked-example.md)
- [cue-omni-reader 配置说明](https://cuecue.cn/hub/omni-reader)
- [cue-research 凭据说明](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands]

**Output Format:** [Markdown 工作稿、事实与证据表格、递交待办；可选 Word (.docx) 文书稿]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [个案事实按出处等级记录，缺失信息保留为待核项；法条、期限及金额须在递交前核验。]

## Skill Version(s):

0.3.10 (source: release evidence; CHANGELOG dated 2026-10-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
