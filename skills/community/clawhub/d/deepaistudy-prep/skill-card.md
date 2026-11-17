## Description:

Generates interactive SVG preview slides and quiz courseware from textbook PDFs or OCR images for selected subjects and grade levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoneyshum](https://clawhub.ai/user/stoneyshum)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, learning-content creators, and students use this CLI to upload textbook PDFs or images, create AI-generated preview lessons, and retrieve OCR text, interactive SVG slides, rendered slide images, quizzes, and knowledge points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords are stored plainly by the CLI configuration flow.

Mitigation: Use a dedicated account or unique password for this service, protect the local config file, and remove stored credentials when the skill is no longer needed.

Risk: Credentials and learning materials can be sent to a loosely configured server endpoint.

Mitigation: Use only https://www.deepaistudy.com or a trusted local loopback server, and avoid arbitrary HTTP or untrusted hosts.

Risk: Uploaded textbook PDFs and images are processed by the configured service.

Mitigation: Upload only materials the user is allowed to share and avoid sensitive student, account, or institutional data in source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stoneyshum/skills/deepaistudy-prep)
- [DeepAIStudy service](https://www.deepaistudy.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [CLI text plus generated SVG/PNG learning materials and quiz/result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured server credentials; uploaded PDFs and images are sent to the configured DeepAIStudy service for processing.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
