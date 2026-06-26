## Description: <br>
用于起草、改写和复核中文公文及正式工作材料；当用户要求通知、请示、报告、函、复函、批复、意见、决定、决议、议案、公报、命令、公告、通告、公示、通报、纪要、方案、说明、申请、征求意见函、采购公告、可研、调研、总结、工作要点、审查材料、讲话稿、致辞、述职报告等中文正式文本，或需要顺稿、压缩、去口语化、降 AI 味、文种校验、办理要素核对时使用。不用于英文、文学、营销、社媒、批量语料或替代法律/财务/采购/审计判断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to draft, revise, and review Chinese official documents and formal work materials such as notices, requests, reports, letters, plans, feasibility studies, speech drafts, and AI-compute procurement or rental materials. It supports document-genre routing, handling-element checks, formal style review, anti-AI-phrasing review, compression, and format-oriented preflight guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document guidance may be mistaken for legal, procurement, finance, audit, confidentiality, or formal signing approval. <br>
Mitigation: Use outputs as drafting and review assistance only, and require qualified human review before relying on sensitive, official, or approval-bearing materials. <br>
Risk: Generated official-document drafts can omit required facts, preserve unresolved placeholders, or include unsupported dates, data, or conclusions. <br>
Mitigation: Check handling elements, missing-information notes, source traceability, and final placeholders before circulation or signing. <br>
Risk: The optional local prose lint script reports writing risks but does not prove correctness or compliance. <br>
Mitigation: Treat lint findings as advisory signals and combine them with manual review against the relevant document genre, format requirements, and organizational process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongyu0918-debug/skills/chinese-official-writing) <br>
- [AI 算力与技术服务材料](references/ai-compute-docs.md) <br>
- [反 AI 表达检查](references/anti-ai-patterns.md) <br>
- [论证链条](references/argument-chains.md) <br>
- [总审层级](references/final-review-layers.md) <br>
- [GB/T 9704-2012 常用格式参考](references/format-gbt9704.md) <br>
- [文种清单](references/genre-checklist.md) <br>
- [文种路由](references/genre-routing.md) <br>
- [办理要素](references/handling-elements.md) <br>
- [公文语言风格](references/official-style.md) <br>
- [复核清单](references/review-checklist.md) <br>
- [写作流程](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text, with optional shell commands and configuration snippets when installation, linting, or agent setup is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include drafted Chinese official-document text, review findings, risk levels, revision suggestions, checklists, missing-information notes, or local lint findings; legal, procurement, finance, audit, confidentiality, and signing decisions require human review.] <br>

## Skill Version(s): <br>
1.4.8 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
