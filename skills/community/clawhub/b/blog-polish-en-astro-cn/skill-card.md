## Description: <br>
Polish and translate a technical blog draft into a 1000-1200 word, 4-5 section Markdown article in English and Simplified Chinese (zh-CN), preserving technical terms and code blocks, then convert the English edition into Astro-compatible Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to polish Markdown blog drafts, translate them into Simplified Chinese, and prepare an Astro-compatible English Markdown version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses unsafe shell evaluation on the user-controlled outputDir before writing files. <br>
Mitigation: Review before installing, use only trusted draft paths and simple output directories, and avoid shell-like values such as command substitutions in outputDir. <br>
Risk: The skill writes Markdown files and creates an images folder in the chosen output directory. <br>
Mitigation: Run it in a workspace where those file writes are expected, and review the generated paths before using the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-polish-en-astro-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files] <br>
**Output Format:** [Markdown files plus a JSON object containing engOutputPath, chnOutputPath, and astroPath] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates English, Simplified Chinese, and Astro Markdown outputs under outputDir, and creates an images folder for the Astro output.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
