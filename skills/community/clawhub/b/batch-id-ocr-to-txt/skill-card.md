## Description:

batch-id extracts name, sex, and ID number fields from up to 50 Chinese ID card image URLs using Tencent Cloud OCR and returns a plain text file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linyao58](https://clawhub.ai/user/linyao58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to process batches of Chinese ID-card front images and produce a copyable text attachment containing extracted identity fields. It is intended for workflows where the user is authorized to process those documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive government ID data and sends image URLs to Tencent Cloud OCR.

Mitigation: Install and run it only when authorized to process the documents, disclose the third-party OCR processing path, and treat the returned text file as sensitive personal data.

Risk: The generated text file can persist extracted identity data after delivery.

Mitigation: Use unique secure temporary output paths or in-memory attachments where supported, clean up generated files after delivery, and restrict access to output storage.

Risk: The dependency declaration allows any tencentcloud-sdk-python version at or above 3.0.0.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linyao58/skills/batch-id-ocr-to-txt)
- [Tencent Cloud CAM API key management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text, files, configuration]

**Output Format:** [Plain text .txt attachment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 50 image URLs are processed per run; each recognized document is formatted as name, sex, and ID number with blank lines between documents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact skill.yaml declares 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
