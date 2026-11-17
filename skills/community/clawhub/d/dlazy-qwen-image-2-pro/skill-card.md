## Description:

Generates images with Alibaba Bailian’s Qwen Image 2.0 Pro model, including designs with detailed scenes and mixed text and imagery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can generate images from text prompts, with optional reference images, for layouts that combine text and imagery. The skill sends requests to dLazy’s hosted service and returns generated image URLs or saved image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that the reported command performs login while the documented purpose is image generation; the scan was partial and did not establish the command’s destination or relationship to the service.

Mitigation: Review the CLI help and verify the command and service destination before use; avoid sending prompts or files until those data flows are understood.

Risk: Prompts and supplied reference images are sent to dLazy-hosted services, and generated assets are hosted there.

Mitigation: Avoid sending sensitive prompts or images, and review the service’s terms and data handling before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-qwen-image-2-pro)
- [dLazy service](https://dlazy.com)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [CLI repository link listed in skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Image files, JSON]

**Output Format:** [JSON response containing generated image URLs; optionally saved image files (PNG shown in the documented example)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image size can be selected from supported presets; asynchronous mode can return a task identifier.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
