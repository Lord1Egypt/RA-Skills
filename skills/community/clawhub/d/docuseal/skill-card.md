## Description: <br>
Manage DocuSeal e-signature workflows from the terminal with the DocuSeal CLI, including template creation, document sending, submission tracking, and submitter updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbturchyn](https://clawhub.ai/user/alexbturchyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they want an agent to prepare and run DocuSeal CLI commands for e-signature workflows in a shell, script, or CI/CD context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent operate an authenticated DocuSeal account, including creating submissions, sending signing requests, archiving records, and updating submitters. <br>
Mitigation: Review generated commands, template IDs, submitter IDs, recipient addresses, and action flags before execution, and use appropriately scoped credentials. <br>
Risk: Documents, remote document URLs, HTML templates, signer contact details, metadata, and message contents may be sent to DocuSeal. <br>
Mitigation: Use trusted document sources, avoid unnecessary sensitive data, and confirm that the selected DocuSeal server and account are appropriate before sending. <br>
Risk: Commands can trigger external emails, SMS messages, payment fields, or signer completion state changes. <br>
Mitigation: Confirm recipient lists, billing-relevant fields, and completion-related flags with a human reviewer before running those commands. <br>


## Reference(s): <br>
- [DocuSeal homepage](https://www.docuseal.com) <br>
- [DocuSeal CLI source](https://github.com/docusealco/docuseal-cli) <br>
- [DocuSeal API keys](https://console.docuseal.com/api) <br>
- [Embedded PDF and DOCX field tags](https://www.docuseal.com/guides/use-embedded-text-field-tags-in-the-pdf-to-create-a-fillable-form) <br>
- [HTML fillable form guide](https://www.docuseal.com/guides/create-pdf-document-fillable-form-with-html-api) <br>
- [DOCX dynamic content variables](https://www.docuseal.com/guides/use-dynamic-content-variables-in-docx-to-create-personalized-documents) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI commands return JSON and require DOCUSEAL_API_KEY, DOCUSEAL_SERVER, and the docuseal binary.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
