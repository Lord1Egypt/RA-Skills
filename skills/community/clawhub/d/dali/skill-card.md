## Description:

Dali by Lulu scores image and video generation prompts, identifies missing elements, and helps rewrite low-scoring prompts with model-specific guidance before generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-the-narwhal](https://clawhub.ai/user/lulu-the-narwhal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill before image or video generation to evaluate prompt quality, identify missing prompt details, and prepare stronger model-specific prompts before spending generation credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts can be sent automatically to an external Dali service, which may expose confidential creative briefs, unreleased product details, personal information, or client material.

Mitigation: Review prompts for sensitive information before use and keep direct control of scoring and generation when confidentiality matters.

Risk: The skill may rewrite low-scoring prompts and use the rewritten prompt for generation without clear user consent.

Mitigation: Review the enhanced prompt and score verification before generation, especially when the prompt encodes brand, legal, client, or safety-sensitive requirements.

## Reference(s):

- [Dali MCP endpoint](https://dali.getlulu.dev/mcp)
- [Dali by Lulu on ClawHub](https://clawhub.ai/lulu-the-narwhal/skills/dali)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown with prompt grades, missing elements, verdicts, rewrite notes, and enhanced prompts in code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a score delta and verification result after re-scoring an enhanced prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
