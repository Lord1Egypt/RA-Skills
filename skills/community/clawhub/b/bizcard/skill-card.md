## Description:

Business card scanner and Google Contacts manager that detects card images, extracts contact fields with OCR, asks for user confirmation, and saves contacts with configurable name formatting and card photos.

This skill is for research and development only.

## Publisher:

[project820](https://clawhub.ai/user/project820)

### License/Terms of Use:

CC BY-NC 4.0

## Use Case:

External users and operators use this skill to process business-card images in OpenClaw, review extracted contact details, and create or update Google Contacts with optional Korean name conventions and card photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-card images and extracted personal contact details are sent to external OCR/image services and the Maton Google Contacts gateway.

Mitigation: Install only where that data flow is acceptable, use the documented dedicated bot or workspace pattern, and review extracted contact details before saving.

Risk: The skill can write or update Google Contacts after confirmation, including contact photos.

Mitigation: Keep user confirmation in the workflow, maintain the Google Contacts OAuth connection intentionally, and disable card photos or name-format options when they do not match the deployment workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/project820/skills/bizcard)
- [People API fields reference](artifact/references/people-api-fields.md)
- [Google People API](https://developers.google.com/people/api/rest)
- [Google People API: createContact](https://developers.google.com/people/api/rest/v1/people/createContact)
- [Google People API: updateContactPhoto](https://developers.google.com/people/api/rest/v1/people/updateContactPhoto)
- [Google People API: searchContacts](https://developers.google.com/people/api/rest/v1/people/searchContacts)
- [OpenClaw installation](https://docs.openclaw.ai/install)
- [Maton settings](https://maton.ai/settings)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON structures and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make external OCR, image-generation, Maton gateway, and Google Contacts calls after user confirmation.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
