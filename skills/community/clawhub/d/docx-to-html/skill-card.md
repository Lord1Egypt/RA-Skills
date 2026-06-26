## Description: <br>
Converts Microsoft Word DOCX files into semantic HTML for browser viewing, content extraction, search, and AI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibekyess](https://clawhub.ai/user/bibekyess) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to convert DOCX documents into clean HTML that can be viewed in browsers, indexed, summarized, or integrated into web and AI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python and Node.js scripts run on user-selected DOCX files and write generated HTML to a chosen output path. <br>
Mitigation: Use only DOCX files intended for processing, choose an output path you control, and inspect the generated HTML before sharing or indexing it. <br>
Risk: Generated HTML may contain sensitive document content or embedded images from the source DOCX. <br>
Mitigation: Delete generated files that contain sensitive content when they are no longer needed. <br>
Risk: The converter depends on npm packages installed locally. <br>
Mitigation: Install dependencies only if you are comfortable running local npm packages for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibekyess/docx-to-html) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [HTML file plus Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python and Node.js scripts; generated HTML should be reviewed before sharing or indexing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
