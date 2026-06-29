## Description: <br>
用于起草、改写和复核中文公文及正式工作材料；当用户要求通知、请示、报告、函、复函、批复、意见、决定、决议、议案、公报、命令、公告、通告、公示、通报、纪要、方案、说明、申请、征求意见函、采购公告、可研、调研、总结、工作要点、审查材料、讲话稿、致辞、述职报告等中文正式文本，或需要顺稿、压缩、去口语化、降 AI 味、文种校验、办理要素核对时使用。不用于英文、文学、营销、社媒、批量语料或替代法律/财务/采购/审计判断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users who draft or review Chinese official work documents use this skill to route document types, check required handling elements, revise style, and produce formal Chinese drafts or review guidance while keeping legal, financial, procurement, audit, and signing judgments under human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated official-document drafts may contain incorrect or misleading legal, financial, procurement, audit, signing, date, document-number, name, or formatting details. <br>
Mitigation: Manually verify those details and route final documents through the responsible human review process before relying on, signing, or filing them. <br>
Risk: The optional lint script can be run against sensitive local documents. <br>
Mitigation: Run linting only in trusted local environments and keep sensitive drafts within the user's approved document-handling workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongyu0918-debug/skills/chinese-official-writing) <br>
- [AI 算力与技术服务材料](references/ai-compute-docs.md) <br>
- [反 AI 表达检查](references/anti-ai-patterns.md) <br>
- [论证链条](references/argument-chains.md) <br>
- [总审层级](references/final-review-layers.md) <br>
- [敬谦称谓和机关用语](references/formal-addressing.md) <br>
- [GB/T 9704-2012 常用格式参考](references/format-gbt9704.md) <br>
- [文种清单](references/genre-checklist.md) <br>
- [文种路由](references/genre-routing.md) <br>
- [办理要素](references/handling-elements.md) <br>
- [公文语言风格](references/official-style.md) <br>
- [复核清单](references/review-checklist.md) <br>
- [写作流程](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown Chinese official-document drafts, review notes, and optional lint command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference a local lint script for draft risk checks; the script reports findings and does not rewrite text.] <br>

## Skill Version(s): <br>
1.4.11 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
