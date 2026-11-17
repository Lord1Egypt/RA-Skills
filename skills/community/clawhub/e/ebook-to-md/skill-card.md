## Description:

Convert PDF/PNG/JPEG/MOBI/EPUB to Markdown using Baidu OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whille](https://clawhub.ai/user/whille)

### License/Terms of Use:


## Use Case:

Developers, analysts, and content migration teams use this skill to convert scanned PDFs, images, MOBI, and EPUB files into Markdown for agent-readable document processing and reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and images may be uploaded to Baidu OCR during conversion.

Mitigation: Use the skill only with documents approved for that provider, and avoid sensitive, regulated, or confidential files unless the deployment has appropriate privacy controls.

Risk: The skill may fetch URLs returned in OCR parsing output when processing Markdown images.

Mitigation: Run it in a network-restricted environment or patch URL fetching to allow only trusted hosts before processing untrusted documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whille/skills/ebook-to-md)
- [Baidu OCR API endpoint](https://aip.baidubce.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown content, optional .md file output, and concise success or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inline extracted images as base64 or write referenced image files next to the Markdown output.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
