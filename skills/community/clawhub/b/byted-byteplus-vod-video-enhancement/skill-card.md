## Description:

Uploads local or URL-based video and audio media to BytePlus VOD, returns playback references, and can start AI-based comprehensive quality restoration for uploaded videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and media workflow operators use this skill to ingest local files or public media URLs into BytePlus VOD and to request video quality restoration jobs that return reusable media references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill signs API requests with BytePlus credentials and uploads selected media and metadata to BytePlus VOD.

Mitigation: Use scoped credentials, inspect the .env file before execution, and run the skill only from a trusted working directory with media the user intends to upload.

Risk: Environment configuration can redirect signed requests or playback URL generation.

Mitigation: Allow only approved BytePlus or Volcengine endpoints and playback domains, especially when VOD_HOST or VOD_PLAY_DOMAIN is set.

Risk: Fetching playback information may publish a remote media asset as a side effect.

Mitigation: Confirm that publication is acceptable before requesting playback URLs, and review the VOD space's access controls for sensitive media.

## Reference(s):

- [BytePlus VOD Python SDK](https://docs.byteplus.com/en/docs/byteplus-vod/docs-python-sdk)
- [Comprehensive Quality Restoration Parameter Reference](references/quality-enhance.md)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON results with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns vid:// and directurl:// media references, playback URLs when available, and resume commands for long-running upload or enhancement jobs.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
