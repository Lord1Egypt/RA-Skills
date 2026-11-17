## Description:

Extracts name, sex, and ID number from batches of front-side ID-card images using Tencent Cloud OCR and returns a formatted TXT file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linyao58](https://clawhub.ai/user/linyao58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to process up to 50 ID-card images at a time and export the extracted identity fields into a downloadable text file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ID-card images and extracted identity details are highly sensitive personal data.

Mitigation: Use the skill only with authorization and consent, and process only the minimum images needed.

Risk: Images are sent to Tencent Cloud OCR for processing.

Mitigation: Confirm that this external processing path satisfies the user's security, privacy, and data residency requirements before use.

Risk: The generated TXT attachment contains full identity details in plaintext.

Mitigation: Restrict access to the attachment, avoid unnecessary retention, and delete the file after delivery or review.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linyao58/skills/batch-id)
- [Tencent Cloud CAM API credentials](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plaintext TXT attachment plus short status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes up to 50 front-side ID-card image URLs and includes extracted identity details in plaintext.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact skill.yaml reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
