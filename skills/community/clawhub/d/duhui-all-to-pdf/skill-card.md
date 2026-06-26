## Description: <br>
Converts a single local Office, WPS, OFD, image, text, or web document to PDF through Duhui's Alibaba Cloud Marketplace asynchronous API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhuitech](https://clawhub.ai/user/duhuitech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to convert one local document to a PDF by uploading it to Duhui/Alibaba-hosted services, submitting an asynchronous conversion job, polling for completion, and saving the returned PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected source documents are uploaded to Duhui/Alibaba-hosted services for conversion. <br>
Mitigation: Use the skill only for documents that can be sent to that third-party infrastructure, and avoid confidential files unless the vendor's retention and privacy terms meet the user's requirements. <br>
Risk: DUHUI_ALI_APPCODE is required for API access and could be exposed if pasted into chat or logs. <br>
Mitigation: Keep DUHUI_ALI_APPCODE in a secure environment variable or secret store, and do not echo it in chat, logs, or final responses. <br>
Risk: Remote temporary source-file cleanup is best effort, so failed cleanup may leave the uploaded source file temporarily available on vendor-controlled storage. <br>
Mitigation: Use non-sensitive source files or confirm vendor retention terms before conversion; treat cleanup failure as a reason to review the uploaded file's sensitivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duhuitech/duhui-all-to-pdf) <br>
- [Duhui Alibaba Cloud Marketplace listing](https://market.aliyun.com/detail/cmapi00044564) <br>
- [Duhui document-to-PDF reference](references/doc_to_pdf_ali.md) <br>
- [Duhui async conversion endpoint](https://doc2pdf.market.alicloudapi.com/v2/convert_async) <br>
- [Duhui conversion status endpoint](https://api.duhuitech.com/q) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with bash commands; script stdout is JSON and successful runs write one PDF file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, DUHUI_ALI_APPCODE, and network access to Duhui/Alibaba endpoints; progress is emitted on stderr.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
