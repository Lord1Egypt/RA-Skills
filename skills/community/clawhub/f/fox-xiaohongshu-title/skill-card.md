## Description:

Maximize CTR (Click-Through Rate) by leveraging emotional hooks and platform algorithms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinthqod](https://clawhub.ai/user/qinthqod)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media operators use this skill to turn a raw topic or text into Xiaohongshu (RedNote) title options optimized for high click-through appeal. It categorizes the topic, applies platform-style title formulas, and returns five concise title candidates with brief cover image guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally optimized for emotional, click-oriented marketing copy, which can produce titles that overstate benefits or feel too promotional.

Mitigation: Review generated titles for brand fit, factual support, and advertising compliance before publication.

Risk: The skill may activate too broadly if generic topics are routed to it.

Mitigation: Use it when the user explicitly wants Xiaohongshu or RedNote title optimization, or when the target channel is clearly social commerce content.

Risk: Generated titles may contain prohibited absolute, medical, or superstition-related claims.

Mitigation: Apply the included blacklist guidance and validator behavior before using a title externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinthqod/skills/fox-xiaohongshu-title)
- [Strategic Assets](artifact/references.md)
- [Few-Shot Examples Library](artifact/examples.md)
- [Title Validator](artifact/validator.py)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown list of five title options with strategy tags plus brief cover image advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Titles are expected to be concise, visually hooked, and filtered against banned terms.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
