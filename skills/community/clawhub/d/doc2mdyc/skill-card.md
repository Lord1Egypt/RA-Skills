## Description: <br>
Use when the user wants to convert local PDF, DOCX, or PPTX files into Markdown with the packaged doc2md CLI, especially for batch conversion, recursive folder processing, or Windows and Linux command-line usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yance-dev](https://clawhub.ai/user/yance-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to run the packaged doc2md CLI for converting PDF, DOCX, and PPTX documents to Markdown, including batch and recursive folder workflows on Windows or Linux. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends document contents to a configured doc2md API endpoint. <br>
Mitigation: Use only trusted or controlled DOC2MD_API_BASE_URL values and avoid processing sensitive, regulated, or unrelated folders unless that endpoint is approved for the data. <br>
Risk: The skill requires a bearer token for API access. <br>
Mitigation: Treat DOC2MD_BEARER_TOKEN and config-file tokens as secrets and avoid exposing them in logs, shell history, or shared files. <br>
Risk: The documented package references platform-specific CLI binaries. <br>
Mitigation: Confirm the referenced CLI files are present in the received package before installation or use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yance-dev/doc2mdyc) <br>
- [Yance Publisher Profile](https://clawhub.ai/user/yance-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of a CLI that writes converted Markdown outputs to user-selected directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
