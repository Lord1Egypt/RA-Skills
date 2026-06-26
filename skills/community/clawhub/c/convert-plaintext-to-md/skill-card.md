## Description: <br>
Convert a text-based document to markdown following instructions from prompt, or if a documented option is passed, follow the instructions for that option. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and documentation maintainers use this skill to convert plain text or generic documentation into Markdown, optionally following explicit instructions, documented options, or a reference Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit or create Markdown files from source documentation. <br>
Mitigation: Use it only on files intended for conversion and review diffs before accepting changes. <br>
Risk: Pattern-based conversion can continue farther through a document than intended if the stopping point is unclear. <br>
Mitigation: Specify a clear stop point for pattern-based conversions when only part of a file should be changed. <br>
Risk: Reference URL fetching can bring untrusted formatting guidance into the conversion process. <br>
Mitigation: Allow reference URL fetching only for documentation sites the user trusts. <br>


## Reference(s): <br>
- [GitHub Basic Writing and Formatting Syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) <br>
- [Markdown Guide Extended Syntax](https://www.markdownguide.org/extended-syntax/) <br>
- [Azure DevOps Markdown Guidance](https://learn.microsoft.com/en-us/azure/devops/project/wiki/markdown-guidance?view=azure-devops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or edit Markdown files from supplied source files and may use a trusted reference document or trusted documentation URL when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
