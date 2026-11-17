## Description:

Polish and translate a technical blog draft into a 1200-1400 word, 4-5 section Markdown article in Simplified Chinese (zh-CN), preserving technical terms and code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to polish technical blog drafts, translate them into Simplified Chinese, and save the result as a structured Markdown article without images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated filenames can escape the intended output folder and overwrite Markdown files elsewhere.

Mitigation: Sanitize titleSlug and verify the final outputPath remains under outputDir before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-polish-zhcn)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Configuration]

**Output Format:** [Markdown article saved to a file, with a JSON object reporting outputPath]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves code blocks and technical terms; returns the path to the polished Markdown file.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
