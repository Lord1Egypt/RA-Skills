## Description:

Analyze polished zh-CN blog markdown, generate hero + per-section image prompts, embed image placeholders into the markdown, and save updated version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Blog authors and developers use this skill after polishing zh-CN markdown to generate consistent hero and section image prompts, insert image placeholders, and save an illustrated markdown draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected blog markdown is read and sent through the configured LLM/image-generation workflow.

Mitigation: Use only intended drafts as input, verify the selected markdown file before running, and avoid directories containing unrelated private markdown.

Risk: Generated image prompts and placeholders may not match the author's intended emphasis for each section.

Mitigation: Review the illustrated markdown draft and generated prompts before publishing or handing the draft to a downstream renderer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-image-embedder)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [JSON result describing the illustrated markdown path, generated image prompts, and image paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an illustrated markdown draft with embedded image placeholders and associated prompt/path metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
