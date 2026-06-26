## Description: <br>
Drafts and fills SaaS and cloud service agreement templates, including MSAs, order forms, software licenses, pilot agreements, design partner agreements, SLA variants, and AI terms, producing signable DOCX files from Common Paper standard forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to select, interview for, and fill SaaS, cloud service, software license, pilot, design partner, and order-form agreement templates. It supports hosted rendering through Open Agreements or a local CLI path when contract details should remain local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted rendering can send confidential business, legal, or personal contract details to the Open Agreements service. <br>
Mitigation: Confirm the user accepts hosted processing before using Remote MCP, and use the Local CLI path for confidential agreements. <br>
Risk: Agreement drafts or template-filled documents may be incomplete, inaccurate, or unsuitable for signature. <br>
Mitigation: Review generated DOCX files with appropriate counsel before signing or distributing them. <br>
Risk: The Local CLI path executes shell commands using user-supplied values and template-derived data. <br>
Mitigation: Validate output filenames and template names, reject shell metacharacters and control characters in values, use quoted heredocs or JSON files safely, pin the CLI version, and remove temporary value files after rendering. <br>


## Reference(s): <br>
- [Cloud Service Agreement ClawHub listing](https://clawhub.ai/stevenobiajulu/cloud-service-agreement) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [Open Agreements](https://openagreements.org) <br>
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements README](https://github.com/open-agreements/open-agreements#use-with-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON field values, shell commands, and DOCX or preview output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote MCP rendering may return an expiring download URL; local CLI rendering writes a DOCX file; preview-only mode emits Markdown.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
