## Description:

Uploads student error-question images to DeepAIStudy for AI analysis, creates error-book records, tracks mastery, and generates variation exercises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoneyshum](https://clawhub.ai/user/stoneyshum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and education-support agents use this skill to manage a DeepAIStudy error-book workflow for photographed student worksheet mistakes, including upload, status checks, review lists, mastery marking, variation generation, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and student worksheet images with weak safeguards.

Mitigation: Use only a trusted HTTPS DeepAIStudy server, avoid shared machines, and do not use real student work or account credentials until the release is reviewed.

Risk: Uploaded images and extracted worksheet content may be processed and retained remotely.

Mitigation: Treat worksheet images and generated analysis as sensitive data and confirm the DeepAIStudy service retention and privacy terms before use.

Risk: The preview control may not prevent upload or saving.

Mitigation: Do not rely on --preview to block uploads or saved records until the implementation is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stoneyshum/skills/deepaistudy-errors)
- [DeepAIStudy service](https://www.deepaistudy.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: server release evidence and setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
