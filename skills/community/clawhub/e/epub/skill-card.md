## Description: <br>
Use this skill whenever the user wants to read, parse, extract content from, modify, or otherwise process an .epub file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaojizhou](https://clawhub.ai/user/gaojizhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and ebook users use this skill to inspect EPUB structure, extract text, metadata, tables of contents, and images, and make simple EPUB modifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or very large EPUB archives may create extraction or resource-use issues. <br>
Mitigation: Use a fresh per-book extraction folder and inspect archive contents before processing large or untrusted EPUBs. <br>
Risk: The artifact includes a package installation command that may affect the active Python environment. <br>
Mitigation: Review the pip install command and prefer an isolated virtual environment before running it. <br>
Risk: EPUB modification workflows can overwrite or replace user files if paths are reused. <br>
Mitigation: Keep original EPUB files unchanged and write modified outputs to explicit new paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce extracted EPUB folders, text files, cover images, or modified EPUB files when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
