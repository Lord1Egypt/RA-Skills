## Description:

分析 CNIPA 审查意见、对比文件和权利要求差异，形成问题拆解、修改依据和答复草案，并提示由专利代理师复核。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent practitioners and teams preparing CNIPA office-action responses use this skill to parse OA materials, compare cited references with claims, map legal issues, identify amendment support, and draft response materials. Outputs are drafts that must be reviewed by a qualified Chinese patent attorney or patent agent before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patent, legal, confidential, unpublished, privileged, or client-restricted files may be sent to PatSnap/Zhihuiya cloud OCR.

Mitigation: Use cloud OCR only with explicit approval; prefer local or direct text extraction when possible; confirm users are allowed to process the documents through the service.

Risk: API keys or credentials could be exposed when invoking OCR tooling.

Mitigation: Use environment-based credential handling and avoid placing API keys in chat, generated deliverables, or command examples.

Risk: Draft OA response materials may contain incorrect legal or technical reasoning if source documents, OCR output, or tool results are incomplete or misread.

Mitigation: Require every substantive statement to cite supplied source material or verified tool output, and require review by a qualified Chinese patent attorney or patent agent before CNIPA submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/cn-patent-oa-response)
- [Source Map - Patent OA Response](artifact/references/source-map.md)
- [AI60 Cloud OCR service](https://connect.zhihuiya.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown draft materials with structured tables, source citations, risk notes, and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft patent/legal analysis only; professional review is required before CNIPA submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
