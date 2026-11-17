## Description:

Generates new content drafts by analyzing reference URLs, extracting content patterns, gathering user context, creating a meta-prompt, and producing multiple draft variations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentchan](https://clawhub.ai/user/vincentchan)

### License/Terms of Use:


## Use Case:

External users, content creators, marketers, and developers use this skill to turn high-performing reference content into reusable anatomy guides, context questions, meta-prompts, and draft content variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided reference URLs to external web services, including routing Twitter/X links through api.fxtwitter.com.

Mitigation: Use only public reference URLs that are acceptable to share with external services.

Risk: Fetched reference content may contain untrusted or misleading material.

Mitigation: Treat fetched content as source material only and review generated drafts before publishing or reuse.

Risk: The security scan verdict is suspicious because outbound network behavior is understated.

Mitigation: Review the skill before installing and confirm its URL-fetching behavior fits the intended environment.

## Reference(s):

- [Content Deconstructor](references/content-deconstructor.md)
- [Content Anatomy Generator](references/content-anatomy-generator.md)
- [Content Context Generator](references/content-context-generator.md)
- [Meta Prompt Generator](references/meta-prompt-generator.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown files containing content breakdowns, anatomy guides, context questions, meta-prompts, and draft variations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates timestamped workflow artifacts and exactly 3 draft variations per requested content type.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
