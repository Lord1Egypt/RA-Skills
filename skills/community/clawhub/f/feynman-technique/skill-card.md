## Description:

Guides an agent through testing understanding of a concept by eliciting a plain-language explanation, diagnosing gaps, and refining the explanation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and practitioners use the skill to check whether they can explain, predict, and apply a specific concept, and to identify what they need to study next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic startup retrieval can introduce remotely changed instructions without user review.

Mitigation: Prefer a reviewed copy with automatic startup retrieval disabled, and approve instruction updates separately.

Risk: The publisher can observe request timing and fetch-client metadata, and learning examples may contain private details.

Mitigation: Avoid private details in learning examples.

## Reference(s):

- [Publisher skill page](https://clawhub.ai/deciqai/skills/feynman-technique)
- [Primary sources](artifact/references/sources.md)
- [The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/)
- [Rogers Commission, Appendix F](https://science.ksc.nasa.gov/shuttle/missions/51-l/docs/rogers-commission/Appendix-F.txt)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a structured Feynman Understanding Audit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures an initial explanation, gap diagnosis, sources consulted, a refined explanation, analogy limits, and an understanding summary.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
