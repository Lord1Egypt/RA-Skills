## Description:

Divide Agent helps agents decompose a user's problem into two MECE layers and present the result as a Mermaid tree and wiki document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to break a task or problem into mutually exclusive, collectively exhaustive sub-problems. It is useful for structured planning when the desired output is a two-layer decomposition, Mermaid tree, and wiki document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wiki documents and submitted attachments may contain private or sensitive information from the original task.

Mitigation: Review generated content before submission when the host environment allows it, and avoid providing sensitive input unless the workflow requires it.

Risk: A MECE decomposition may be incomplete, overlapping, or unsuitable for downstream planning.

Mitigation: Review the proposed sub-problems and Mermaid tree before relying on them for decisions or follow-on work.

## Reference(s):

- [Porter's Five Forces reference](https://zhida.zhihu.com/search?content_id=245774722&content_type=Article&match_order=1&q=五力&zhida_source=entity)
- [3C reference](https://zhida.zhihu.com/search?content_id=245774722&content_type=Article&match_order=1&q=3C&zhida_source=entity)
- [7S reference](https://zhida.zhihu.com/search?content_id=245774722&content_type=Article&match_order=1&q=7S&zhida_source=entity)
- [PPM Matrix reference](https://zhida.zhihu.com/search?content_id=245774722&content_type=Article&match_order=1&q=PPM%E7%9F%A9%E9%98%B5&zhida_source=entity)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with Mermaid syntax and a generated wiki document attachment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Second-layer decomposition is limited to at most three sub-problems.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
