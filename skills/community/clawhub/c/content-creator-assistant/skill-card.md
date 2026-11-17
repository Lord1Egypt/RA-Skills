## Description:

AI writing assistant using Reflection + Tree of Thoughts for high-quality content creation. Generates articles, blogs, and documentation with iterative refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banxian87](https://clawhub.ai/user/banxian87)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate and refine articles, blog posts, documentation, marketing copy, and social media content from a topic, audience, tone, length, and key points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing prompts and draft text are sent to the configured LLM implementation.

Mitigation: Use an LLM provider and deployment path approved for the sensitivity of the input content.

Risk: The release evidence notes a packaging mismatch that may affect functionality.

Mitigation: Fix and test package import paths before relying on the skill in production workflows.

Risk: Generated content can contain inaccurate, incomplete, or misleading statements.

Mitigation: Review generated drafts for factual accuracy, policy compliance, and audience fit before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banxian87/skills/content-creator-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown content and structured JavaScript return values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title, content, word count, outline, draft, and iteration count.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
