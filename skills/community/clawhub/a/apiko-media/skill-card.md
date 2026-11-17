## Description:

Generate or edit images and generate videos through the APIKO API, with support for asynchronous jobs, polling, and saving results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tong0619453646-dev](https://clawhub.ai/user/tong0619453646-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or edit images and generate videos with APIKO models. It helps select models, check costs, submit and monitor asynchronous jobs, and save results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags potential API-key exposure to an unintended destination and an unpinned package command; the scan was partial.

Mitigation: Review API-key handling and package-install instructions before use, verify that the API destination is trusted, and assess whether to pin the package version.

Risk: Uploaded reference images are publicly accessible to anyone with their URL for 72 hours.

Mitigation: Upload only reference images that are safe to share publicly, and obtain consent before uploading private or sensitive images.

## Reference(s):

- [APIKO Media source (server-resolved provenance)](https://github.com/tong0619453646-dev/apiko-ai-api-examples/tree/main/skills/apiko-media)
- [APIKO Media on ClawHub](https://clawhub.ai/tong0619453646-dev/skills/apiko-media)
- [APIKO API documentation](https://apiko.app/docs)
- [APIKO models](https://apiko.app/models)
- [Model notes](references/models.md)

## Skill Output:

**Output Type(s):** [Image files, Video files, Shell commands, Guidance]

**Output Format:** [Generated image or video files, with JSON task details and Markdown guidance containing shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media type and file format depend on the selected model; jobs run asynchronously.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
