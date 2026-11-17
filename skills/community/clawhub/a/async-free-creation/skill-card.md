## Description:

Calls Flyelep's asynchronous Image-2 free-creation API to generate product or creative images from a prompt and optional reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit Flyelep Image-2 image generation jobs, poll for completion, and return generated image URLs for product or creative image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, API keys, and reference images are sent to Flyelep during use.

Mitigation: Obtain the API key from the user at runtime, avoid storing it, and exclude confidential, regulated, personal, or unreleased information from prompts and reference images unless the user accepts the transfer.

Risk: Uploaded local reference images may be converted into permanent unsigned public URLs without a clear deletion or revocation path.

Mitigation: Use existing public image URLs when possible, upload only material approved for public or third-party handling, and tell users that returned upload URLs may remain accessible to anyone who receives them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyelepai/skills/async-free-creation)
- [Flyelep Open Platform](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with HTTP request examples, JSON payloads, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include asynchronous task IDs, polling status, and public image result URLs.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
