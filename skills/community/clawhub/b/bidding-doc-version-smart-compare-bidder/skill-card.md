## Description:

当用户上传两份招标文件（docx/pdf，含文本层）需要比对版本差异、标注变更对投标的影响时触发；从投标人视角分析差异条款的投标影响（报价、技术方案、资格、时限权利），输出结构化差异报告，仅支持中文可编辑文档，不支持扫描件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and bid teams use this skill to compare an original Chinese tender document with a revised, addendum, or clarification version and understand how each change affects pricing, technical response, qualification preparation, deadline rights, and compliance risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender documents can contain confidential or commercially sensitive bidding information.

Mitigation: Install and run the skill in a dedicated approved environment and keep source documents, extracted text, and reports within the user's authorized workspace and knowledge-base policy.

Risk: The generated report may miss differences or overstate legal or procurement impact, especially with complex layout, weak PDF text extraction, or incomplete knowledge-base hits.

Mitigation: Treat outputs as an aid only; manually review critical clauses, red-line findings, deadline calculations, and high-value bidding decisions before acting.

Risk: Unsupported scanned PDFs, image-only files, encrypted files, very large documents, or non-Chinese documents can produce incomplete or failed analysis.

Mitigation: Use DOCX or text-layer PDF inputs under the documented size limit, request editable source files when needed, and apply OCR outside the skill before rerunning if the source is image-only.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/chesaram/skills/bidding-doc-version-smart-compare-bidder)
- [Stage 3 Difference Detection Rules](references/stage3_diff.md)
- [Stage 4 Bidder Impact Classifier](references/bidder/stage4_classify.md)
- [Stage 5 Bidder Review and Timeliness Checks](references/bidder/stage5_review.md)
- [Output Schema](references/output_schema.md)
- [Golden Longling Regression Dataset](references/golden_longling_4vs5.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional DOCX report and intermediate JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include structured tender-difference findings, risk summaries, bidder action guidance, pricing and deadline notes, and disclaimers requiring human review for high-stakes conclusions.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
