## Description: <br>
小方同学全球首个营销方案Agent helps an agent create structured marketing plans and export polished PPT-style deliverables from a topic, file, or link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaok8700](https://clawhub.ai/user/xiaok8700) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill to turn a marketing topic, source document, or web link into a staged marketing plan, then generate presentation images and downloadable report files through the AIPPT service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles AIPPT authentication and may expose account credentials or tokens during agent-driven login. <br>
Mitigation: Avoid entering an AIPPT password through the agent; prefer QR login where possible and limit use to accounts authorized for this workflow. <br>
Risk: Generated reports, PDFs, and QR login images may be uploaded to tmpfiles.org links accessible to anyone with the URL. <br>
Mitigation: Do not use confidential business plans, customer data, or sensitive credentials in generated content, and share returned download links only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaok8700/aippt-marketing) <br>
- [AIPPT homepage](https://www.aippt.cn) <br>
- [API details](references/api-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with API command examples, generated presentation images, and downloadable PDF or report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AIPPT account, member credits, browser access for QR login, and command execution for API calls and file generation.] <br>

## Skill Version(s): <br>
1.2.9 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
