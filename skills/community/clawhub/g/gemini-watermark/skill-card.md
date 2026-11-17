## Description:

Removes visible Gemini AI star/sparkle watermarks from images using reverse alpha blending, with single-image and batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h1bomb](https://clawhub.ai/user/h1bomb)

### License/Terms of Use:


## Use Case:

Developers and automation users can use this skill to run local Python workflows that remove visible Gemini watermarks from individual images or batches of images when they have rights to do so.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remove visible AI provenance marks from images that may be shared or published.

Mitigation: Use it only when you have clear rights and when removal does not violate platform terms, licensing terms, or disclosure expectations.

Risk: Cleaned images may be redistributed without adequate provenance or AI-generation disclosure.

Mitigation: Preserve appropriate disclosure and provenance information when publishing or sharing outputs.

Risk: Dependency installation can introduce supply-chain exposure.

Mitigation: Install dependencies in an isolated environment and prefer pinned, reviewed versions.

## Reference(s):

- [Gemini Watermark Removal Algorithm](references/algorithm.md)
- [Removing Gemini AI Watermarks: A Deep Dive into Reverse Alpha Blending](https://allenkuo.medium.com/removing-gemini-ai-watermarks-a-deep-dive-into-reverse-alpha-blending-bbbd83af2a3f)
- [GeminiWatermarkTool reference implementation](https://github.com/allenk/GeminiWatermarkTool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may lead to local image file outputs when the bundled script is run.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
