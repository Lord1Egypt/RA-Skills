## Description:

Indexes a Bilibili AI Agent tutorial reference into a local learning knowledge base for LLM and agent study.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to trigger a Bilibili AI Agent tutorial reference with llm/agent keywords and add related learning text to a local knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user-supplied text into a local knowledge base.

Mitigation: Review inputs before running, avoid sensitive text, and use it only when local storage is intended.

Risk: The skill depends on an undeclared local Python module under D:\\coze-local\\db.

Mitigation: Install only in environments where that local dependency is trusted, present, and auditable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/534422530/skills/auto-llm-4840)
- [Bilibili Source Video](https://www.bilibili.com/video/BV11NNAz5EKn)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text learning reference with a local knowledge-base update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist provided input in a local knowledge base.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
