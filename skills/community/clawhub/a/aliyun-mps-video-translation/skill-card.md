## Description:

Use when creating or managing Alibaba Cloud IMS video translation jobs via OpenAPI for subtitle, voice, and face translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to submit, poll, and manage Alibaba Cloud IMS video translation jobs through OpenAPI. It supports workflows for subtitles, translated speech, face translation, OSS input and output configuration, and job evidence capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials can access IMS/MPS and OSS resources if over-permissioned.

Mitigation: Use credentials limited to the IMS/MPS and OSS resources required for the current video translation task.

Risk: Cloud API usage and media processing jobs can incur costs.

Mitigation: Monitor Alibaba Cloud usage and costs before and after submitting translation jobs.

Risk: DeleteSmartJob can remove managed job records.

Mitigation: Confirm the target job ID and intent before allowing any DeleteSmartJob operation to run.

## Reference(s):

- [Skill source on ClawHub](https://clawhub.ai/cinience/skills/aliyun-mps-video-translation)
- [IMS video translation field reference](references/fields.md)
- [Source list](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API parameter descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request guidance, polling steps, job management instructions, and evidence capture notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
