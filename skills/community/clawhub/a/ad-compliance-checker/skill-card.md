## Description:

对电商图片、视频和文本素材进行两阶段广告合规审查：先进行通用风险快筛，再结合广告合规知识库生成深度分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, e-commerce operators, and reviewers use this skill to screen ad copy, image descriptions, and video materials for common advertising compliance risks and receive specific revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed ad materials may be submitted to external review services through referenced skills.

Mitigation: Confirm data handling requirements before use and avoid submitting sensitive or restricted content unless the external service path is approved.

Risk: Ad text or media descriptions could include adversarial instructions that try to influence the model's review.

Mitigation: Treat submitted ad content as untrusted input and keep review rules separate from the content being analyzed.

Risk: The generated compliance report is advisory and may miss legal or platform-specific requirements.

Mitigation: Have qualified reviewers validate high-risk findings and final advertising decisions before publication.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [Absolute terms knowledge base](artifact/knowledge_base/absolute_terms.md)
- [Efficacy claims knowledge base](artifact/knowledge_base/efficacy_claims.md)
- [Misleading endorsements knowledge base](artifact/knowledge_base/misleading_endorsements.md)
- [Prohibited promises knowledge base](artifact/knowledge_base/prohibited_promises.md)
- [Review prompt template](artifact/prompt_template.txt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown compliance review report with risk ratings, detailed risk analysis, and modification suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output based on submitted ad text, image descriptions, video review results, and the bundled knowledge base]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
