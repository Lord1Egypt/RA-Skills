## Description: <br>
Formats plain text or markdown files with frontmatter, titles, summaries, headings, bold, lists, and code blocks, outputting a formatted markdown file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn plain text or existing markdown into structured, reader-friendly markdown while preserving the author's content. It can add or normalize frontmatter, titles, summaries, headings, emphasis, lists, code formatting, and CJK typography fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite local files or modify the original file directly in typography-only mode. <br>
Mitigation: Run it on copies or in a clean git branch, then review diffs before keeping the result. <br>
Risk: The skill may create extra analysis or backup files and alter article metadata or structure. <br>
Mitigation: Inspect generated analysis, frontmatter, and formatted markdown before publishing or replacing source files. <br>
Risk: The spacing option runs an external formatter through npx. <br>
Mitigation: Disable spacing or review and trust the autocorrect-node execution path before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimliu/baoyu-format-markdown) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-format-markdown) <br>
- [Title Formulas Reference](references/title-formulas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown files plus concise markdown completion report with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically creates an analysis file and a formatted markdown file; typography-only mode can modify the original file in place.] <br>

## Skill Version(s): <br>
1.117.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
