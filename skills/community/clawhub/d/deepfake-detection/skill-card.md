## Description:

Detect deepfakes in images or videos using the Scam.ai API, including API key setup and analysis of user-provided media for face-swap or deepfake manipulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchennnnnnn](https://clawhub.ai/user/yuchennnnnnn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit image or video files for Scam.ai deepfake analysis and receive a concise real, suspicious, or deepfake verdict with confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Scam.ai API key on disk.

Mitigation: Use a service-specific key when possible, restrict file permissions, rotate keys as needed, and delete stored key files when they are no longer required.

Risk: The skill uploads potentially sensitive images or videos to Scam.ai for analysis.

Mitigation: Use only media you are comfortable sending to Scam.ai and review privacy or retention expectations before analyzing sensitive content.

Risk: The security review found insufficient consent and input-safety safeguards around shell-based uploads.

Mitigation: Review the skill before installation, confirm the file path and upload destination before running it, and prefer a revised version that asks before uploads and avoids shell interpolation for keys and paths.

## Reference(s):

- [Scam.ai](https://scam.ai)
- [Scam.ai documentation](https://scam.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown text with optional shell commands and a single-line verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads user-selected media to Scam.ai and summarizes only the verdict and confidence unless more detail is requested.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
