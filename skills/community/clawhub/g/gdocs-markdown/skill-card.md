## Description: <br>
Create Google Docs from Markdown files by converting Markdown to DOCX and uploading the result to Google Drive as an editable Google Doc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techlaai](https://clawhub.ai/user/techlaai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when they need to turn Markdown content into an editable Google Doc using the local gog CLI and Google Drive upload flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script uploads the selected Markdown-derived document to Google Drive using the currently authenticated gog account. <br>
Mitigation: Confirm the active gog account and only run the skill on content intended for Google Docs. <br>
Risk: The helper script downloads Pandoc from GitHub into /tmp when the expected local binary is absent. <br>
Mitigation: Install Pandoc from a trusted package manager before use when tighter supply-chain control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/techlaai/gdocs-markdown) <br>
- [Pandoc 3.1.11 Linux release archive](https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-linux-amd64.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and Google Docs URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Markdown file path and optional document title; the helper script returns the Google Docs link after upload.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
