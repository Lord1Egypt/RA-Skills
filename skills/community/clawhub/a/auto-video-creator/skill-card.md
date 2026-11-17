## Description:

Auto Video Creator generates short videos from text prompts or images using the XLXAI Sora2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yefl2064](https://clawhub.ai/user/yefl2064)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and content teams use this skill to generate short-form video assets from prompts or source images. It supports text-to-video and image-to-video workflows and returns task/result JSON rather than publishing content to social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local path passed with --image can upload any readable local file to the external XLXAI video API without verifying that the file is really an image.

Mitigation: Only pass intended image files; add file type, size, path allowlist, and confirmation checks before using the skill in shared or automated workflows.

Risk: Prompts, source images, and generated video URLs are sent to or returned from an external provider.

Mitigation: Avoid sensitive prompts and private files, keep XLXAI_API_KEY in environment variables or managed secrets, and review provider terms before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yefl2064/skills/auto-video-creator)
- [XLXAI API endpoint](https://api.xlxai.store)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [JSON API task/result payloads with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XLXAI_API_KEY and may return third-party video URLs when generation completes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
