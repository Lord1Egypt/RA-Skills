## Description: <br>
Converts PDF, PNG, JPEG, MOBI, and EPUB files to Markdown using Baidu OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whille](https://clawhub.ai/user/whille) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert scanned PDFs, images, and ebooks into Markdown when Baidu OCR credentials and any required Calibre dependency are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents and images may be sent to Baidu OCR, exposing confidential, regulated, or business-sensitive content. <br>
Mitigation: Use only with files that are approved for Baidu processing and avoid sensitive documents unless the deployment has explicit approval. <br>
Risk: Baidu OCR credentials are required for operation. <br>
Mitigation: Keep BAIDU_OCR_API_KEY and BAIDU_OCR_SECRET_KEY scoped, rotated, and unavailable to unrelated tools or users. <br>
Risk: Parser-returned image URLs may be fetched automatically when inline image handling is enabled. <br>
Mitigation: Review this behavior for untrusted documents and disable inline image handling when automatic image fetching is not acceptable. <br>
Risk: MOBI and EPUB conversion depends on a local Calibre installation. <br>
Mitigation: Install Calibre from a trusted source and keep it updated before processing ebook files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whille/ebook-to-md) <br>
- [Baidu OCR documentation](https://cloud.baidu.com/doc/OCR/s/7mh8u7ruk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files] <br>
**Output Format:** [Markdown content returned as text, with optional .md file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inline images as base64 or write local image references depending on the inline_images setting.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
