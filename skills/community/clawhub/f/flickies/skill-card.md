## Description:

Flickies lets an agent use a self-hosted REST or MCP service to create and edit videos, restore faces, and inspect media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use Flickies to submit video tasks through REST or MCP, including lipsync, face restoration, transcoding, and metadata inspection. It returns media files or task results from the configured self-hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use mutable container image tags, and the scanner reports that the quick-install commands can expose an unauthenticated API.

Mitigation: Set FLICKIES_AUTH_TOKEN, avoid exposing the API without authentication, verify the image source, and pin a trusted image digest before deployment.

## Reference(s):

- [Setup guide](artifact/references/setup.md)
- [Flickies project homepage](https://github.com/psyb0t/docker-flickies)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/flickies)

## Skill Output:

**Output Type(s):** [Video files, JSON responses, API calls, Shell commands]

**Output Format:** [Video and audio media files, JSON API responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media results may be staged for download or delivered to a supplied URL; long tasks can return job status before completion.]

## Skill Version(s):

0.3.18 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
