## Description: <br>
Drafts and fills data privacy agreement templates, including DPAs, HIPAA BAAs, business associate agreements, and AI addenda, and can produce signable DOCX files from Common Paper standard forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to select a data privacy template, collect required field values, and generate a DOCX agreement or markdown preview for review before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agreements may not satisfy a user's jurisdiction, regulatory facts, or signing requirements. <br>
Mitigation: Treat output as a drafting aid and have qualified counsel review the document before signing. <br>
Risk: Template metadata, template content, and user-provided field values can contain prompt-like text. <br>
Mitigation: Treat those inputs as data, reject control characters and excessive lengths, and require explicit user confirmation before filling a template. <br>
Risk: Remote rendering may return an expiring download URL, while local rendering uses temporary files containing agreement field values. <br>
Mitigation: Share links only with intended recipients, use restrictive permissions for local value files, and clean up temporary files after rendering. <br>


## Reference(s): <br>
- [Data Privacy Agreement on ClawHub](https://clawhub.ai/stevenobiajulu/data-privacy-agreement) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [Open Agreements](https://openagreements.org) <br>
- [open-agreements on npm](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements README](https://github.com/open-agreements/open-agreements#use-with-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON field values, shell commands, and DOCX files or expiring download URLs when a renderer is available; markdown preview when not.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a remote MCP, a local CLI, or preview-only mode; requires user confirmation before filling a template.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
