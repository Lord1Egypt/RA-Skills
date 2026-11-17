## Description:

将医药/医疗行业电话会、策略会、专家会或业绩会的原始转写整理为高完整度、买方/卖方内部常用风格的标准化会议纪要。适用于术语纠错、Q&A重构、关键信息保留、低置信度内容与音频时间点标注。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzgztth-debug](https://clawhub.ai/user/lzgztth-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to turn Chinese healthcare, pharma, medical services, device, CXO, strategy, expert, or earnings-call transcripts into structured internal research notes. It emphasizes complete preservation of key facts, careful terminology correction, Q&A reconstruction, and explicit marking of low-confidence content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conference transcripts may contain confidential business, healthcare-sector, or personal information.

Mitigation: Only provide content the user is authorized to process in the agent environment, and remove sensitive details when they are not needed for the notes.

Risk: Terminology correction and Q&A restructuring can change meaning if uncertain transcript fragments are treated as facts.

Mitigation: Preserve uncertainty, mark low-confidence terms or numbers as待确认, and include timestamps or 无可用时间戳 when source material does not provide timestamps.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown meeting notes in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves key numbers, logic chains, Q&A structure, uncertainty markers, and timestamps when available.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
