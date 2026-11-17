## Description:

Provides an agent protocol for using Alibaba Cloud Yike CLI to upload media, generate images and videos, inspect media, recover jobs, and manage authentication and account setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through Yike CLI workflows for cloud media upload, image and video generation, job polling, recovery, media inspection, and account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yike receives the prompts and media submitted through the CLI, and generation or upload workflows may use Yike account credits.

Mitigation: Use the skill only when that data sharing and credit usage are acceptable; review dry-run credit estimates before normal submissions.

Risk: Automatic execution wording can bypass the normal post-estimate confirmation for credit-consuming cloud submissions and uploads.

Mitigation: Avoid phrases such as "do not ask" or "submit directly" unless bypassing confirmation is intended for that task.

## Reference(s):

- [Authentication, Account & Setup](references/account-and-setup.md)
- [Generate Command Family](references/generate.md)
- [Image Generation Operation Reference](references/generate-image.md)
- [Video Generation Operation Reference](references/generate-video.md)
- [Media Inspection & Job Recovery](references/media-and-jobs.md)
- [Local Asset Upload](references/upload.md)
- [Video Model Reference Input Capabilities](references/video-model-capabilities.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-aware command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Yike CLI JSON output to preserve media IDs, job IDs, resume commands, status, URLs, dimensions, durations, file sizes, and warnings.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
