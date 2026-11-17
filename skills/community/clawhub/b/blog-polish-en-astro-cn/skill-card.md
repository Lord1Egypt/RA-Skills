## Description:

Polish and translate a technical blog draft into a 1000-1200 word, 4-5 section Markdown article in English and Simplified Chinese (zh-CN), preserving technical terms and code blocks, then convert the English edition into Astro-compatible Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and blog authors use this skill to turn a draft Markdown technical post into polished English, Simplified Chinese, and Astro-compatible Markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or accidental outputDir value could execute shell commands.

Mitigation: Review outputDir before running the skill; use a trusted directory path and avoid shell metacharacters or untrusted values.

Risk: Generated English, Chinese, Astro, and image-directory outputs may persist derived copies of sensitive drafts.

Mitigation: Use the skill only with drafts suitable for storage in the chosen output directory and confirm the output locations before execution.

Risk: The emitted file path JSON may include more fields than the declared output schema describes.

Mitigation: Check the final JSON for engOutputPath, chnOutputPath, and astroPath, and confirm downstream tooling expects those keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-polish-en-astro-cn)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown files with a JSON path summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces English, Simplified Chinese, and Astro Markdown outputs in the requested output directory.]

## Skill Version(s):

1.0.12 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
