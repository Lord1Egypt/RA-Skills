## Description:

Parses uploaded resume files and extracts structured resume information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51mee-com](https://clawhub.ai/user/51mee-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to convert resumes in PDF, DOC, DOCX, JPG, or PNG format into a consistent structured profile for review or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume files can contain sensitive personal data, including contact details and employment or education history.

Mitigation: Use the skill only in workflows approved for handling resume data, and avoid submitting resumes unless the data handling path is acceptable.

Risk: A resume from an unknown source may include embedded instructions that influence the model output.

Mitigation: Validate parsed JSON before relying on it or passing it to downstream systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/51mee-com/skills/51mee-resume-parse)
- [Publisher profile](https://clawhub.ai/user/51mee-com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON with an optional Markdown presentation structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured resume fields include basic details, contact information, work experience, project experience, education, expected position, keywords, awards, certificates, and professional skills.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
