## Description:

This skill converts a single local Office, WPS, OFD, image, text, HTML, or similar document to PDF through Duhui's Alibaba Cloud Marketplace asynchronous API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duhuitech](https://clawhub.ai/user/duhuitech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks to convert one local document into one PDF through the Duhui/Alibaba asynchronous conversion service. It is suited for workflows that can upload the selected file to third-party cloud infrastructure and need a local PDF result plus structured conversion status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local documents are uploaded to Duhui/Alibaba-controlled infrastructure in the cn-shanghai OSS flow, and the security summary notes that upload consent may be too broad.

Mitigation: Use the skill only after explicit consent for the selected file, prefer local conversion for confidential documents, and restrict network access to the documented endpoints where possible.

Risk: The required DUHUI_ALI_APPCODE is a secret used to authorize conversion requests.

Mitigation: Provide the AppCode through an environment variable or secret store rather than chat, logs, or final responses.

Risk: Remote source cleanup is best-effort, so uploaded source files may remain temporarily if deletion fails.

Mitigation: Avoid sensitive files unless third-party upload and temporary retention are acceptable for the user's workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duhuitech/skills/duhui-all-to-pdf)
- [Alibaba Cloud Marketplace product page](https://market.aliyun.com/detail/cmapi00044564)
- [Duhui document-to-PDF API reference](references/doc_to_pdf_ali.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands; the conversion script writes JSON to stdout and saves a PDF file on success.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, DUHUI_ALI_APPCODE, and network access to the documented Duhui and Alibaba endpoints; progress is written to stderr.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
