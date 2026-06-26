## Description: <br>
Ebook Maker guides an agent through confirming requirements, researching a topic, drafting and laying out an ebook, optionally generating illustrations, and exporting a PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irenerachel](https://clawhub.ai/user/irenerachel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to produce Chinese-language ebook or PDF handbook drafts from a topic, including research, outline confirmation, layout, optional illustrations, and a delivery report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or sensitive credentials may be exposed when checking image-provider configuration. <br>
Mitigation: Check whether required environment variables are present without printing their values, and avoid logging secrets in reports. <br>
Risk: Prompts, ebook topics, and project details may be sent to third-party image providers when illustrations are enabled. <br>
Mitigation: Disable illustration generation for sensitive projects or review and minimize prompts before sending them to an external provider. <br>
Risk: Raw project details and generated artifacts may be stored in predictable Downloads folders. <br>
Mitigation: Use a controlled output directory for sensitive work and remove temporary research, image, HTML, and report files after delivery. <br>
Risk: Generated PDFs may include local path, date, or layout metadata depending on export settings. <br>
Mitigation: Review exported PDFs before sharing and strip unintended metadata or headers when needed. <br>


## Reference(s): <br>
- [Ebook Maker on ClawHub](https://clawhub.ai/irenerachel/ebook-maker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with HTML/CSS snippets, shell commands, and PDF delivery notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local research reports, work reports, downloaded images, HTML drafts, and PDFs when the host agent follows the workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
