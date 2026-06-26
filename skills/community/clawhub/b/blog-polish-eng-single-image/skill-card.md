## Description: <br>
Polish a technical blog draft into a 1000-1200 word, 4-5 section en-US article, preserve technical terms/code, and generate one consistent hero image prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and engineering teams use this skill to turn rough or translated technical markdown drafts into publishable English articles while preserving code, commands, identifiers, and product details. It also prepares one consistent hero image prompt and output path for the finished post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rewrite may unintentionally change technical meaning, commands, code samples, or product details. <br>
Mitigation: Review the polished article against the source draft before publishing, with special attention to code blocks, commands, file paths, URLs, and named APIs. <br>
Risk: The hero image prompt or generated PNG may be off-topic, too literal, or unsuitable for publication. <br>
Mitigation: Review the single-line hero image prompt and generated image before publishing; regenerate or revise the prompt when it does not match the article's subject and tone. <br>
Risk: User-provided or default paths may point to the wrong draft or output directory. <br>
Mitigation: Confirm draftPath, outputDir, and subject before running the skill, especially when working across multiple drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-polish-eng-single-image) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [Markdown article plus structured text fields for polishedPath, imagePath, and imagePrompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates exactly one hero image prompt and a matching PNG path using the same basename as the markdown output.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
