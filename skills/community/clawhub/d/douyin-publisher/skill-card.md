## Description:

Publishes video content to Douyin with a title, description, tags, and optional cover through the Douyin Creator Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viv888-ai](https://clawhub.ai/user/viv888-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to prepare and publish confirmed video posts to Douyin from a local video path or trusted video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish through a saved logged-in browser session.

Mitigation: Use a dedicated Douyin account or browser profile, confirm every post before publishing, and prefer an in-script confirmation gate before final submission.

Risk: The skill downloads arbitrary video URLs without meaningful safety limits.

Mitigation: Use trusted local files or trusted HTTPS video URLs, and add URL validation, download size and time limits, and temporary-file cleanup before deployment.

Risk: The Playwright dependency is lower-bounded rather than pinned.

Mitigation: Pin dependency versions and test the publishing workflow after browser or platform updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viv888-ai/skills/douyin-publisher)
- [Douyin Creator Platform](https://creator.douyin.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
