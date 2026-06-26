## Description: <br>
Polish and translate a technical blog draft into a 1200-1400 word, 4-5 section Markdown article in Simplified Chinese (zh-CN), preserving technical terms and code blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and external users use this skill to polish a technical blog draft and translate it into Simplified Chinese while preserving code blocks and technical terms. It is intended for text-only draft workflows without images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The output filename is partly controlled by a model-generated title slug and is not safely constrained to the chosen output folder. <br>
Mitigation: Keep outputDir inside a safe workspace, check the returned outputPath, and constrain the title slug to simple filename characters before use. <br>
Risk: Draft input may contain sensitive content. <br>
Mitigation: Use only non-sensitive drafts with this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-polish-zhcn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON] <br>
**Output Format:** [JSON object containing outputPath; generated article is saved as a Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Markdown article targets 1200-1400 words and 4-5 sections.] <br>

## Skill Version(s): <br>
1.0.13 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
