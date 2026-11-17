## Description:

Polish a technical blog draft into an 800-1000 word, 3-4 section zh-CN article, preserve technical terms/code, and generate consistent hero and per-section image prompts when the user asks to polish and translate a blog with images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and technical writers use this skill to turn a draft technical blog into a polished Simplified Chinese Markdown article with matching image prompts while preserving code and technical terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the executable workflow may create a simulated result rather than a genuinely polished zh-CN article.

Mitigation: Review the generated Markdown against the original draft and verify translation quality before publishing.

Risk: Drafts and polished outputs are saved under ~/.openclaw by default, which may retain sensitive content locally.

Mitigation: Use a non-sensitive output directory for private drafts or remove generated files after review.

Risk: The artifact can return intended image filenames and prompts without actually generating image files.

Mitigation: Confirm referenced image files exist, or run a separate image-generation step before treating the package as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-polish-zhcn-images)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [JSON containing output paths and image prompt arrays, with Markdown content written to disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is under ~/.openclaw/workspace/contentPolished; image paths may be intended filenames when image generation is unavailable.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
