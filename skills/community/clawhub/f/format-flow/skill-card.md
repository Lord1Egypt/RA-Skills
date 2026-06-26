## Description: <br>
Convert and format documents across Word, PDF, Markdown, web pages, Excel, and images with compression, resizing, and format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sashavegal](https://clawhub.ai/user/sashavegal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content operators use this skill to convert documents between Word, PDF, Markdown, HTML, Excel, JSON, and common image formats. It is suited for document publishing, text extraction, batch format migration, web-page capture, and lightweight image preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install unpinned Python packages when its conversion script runs. <br>
Mitigation: Run it in a virtual environment with dependencies reviewed, preinstalled, and pinned before use in shared or production environments. <br>
Risk: The web-to-Markdown workflow can fetch user-supplied URLs. <br>
Mitigation: Avoid processing sensitive internal URLs unless the operator intends the skill to retrieve and convert that content. <br>
Risk: Batch and recursive modes can process many files from selected folders. <br>
Mitigation: Use batch or recursive modes only on deliberately selected directories and review outputs before distributing converted files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sashavegal/format-flow) <br>
- [Publisher profile](https://clawhub.ai/user/sashavegal) <br>
- [Pandoc installation guide](https://pandoc.org/installing.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, DOCX, PDF, image files, and plain text produced through command-line workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process single files or selected folders in batch and recursive modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
