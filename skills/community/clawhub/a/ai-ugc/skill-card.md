## Description:

AI UGC helps agents call RawUGC API endpoints to generate AI videos, images, and music, manage creative assets, schedule social posts, research TikTok content, and analyze viral videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tfcbot](https://clawhub.ai/user/tfcbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate RawUGC workflows for AI media generation, media management, social scheduling, and TikTok research through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a RawUGC API key and RawUGC-connected social accounts.

Mitigation: Install only when that access is acceptable, keep RAWUGC_API_KEY secret, and avoid logging or hardcoding the key.

Risk: The skill can disconnect accounts, delete resources, change scheduled posts, or publish immediately.

Mitigation: Require explicit user confirmation before deletes, account disconnects, scheduling changes, and publish-now actions.

Risk: Uploaded media may become public URLs and is processed by RawUGC.

Mitigation: Avoid uploading sensitive media and review any media URL before using it in generation or analysis workflows.

## Reference(s):

- [RawUGC API base URL](https://rawugc.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/tfcbot/skills/ai-ugc)
- [ClawHub publisher profile](https://clawhub.ai/user/tfcbot)
- [Clawdis homepage](https://github.com/tfcbot/rawugc-skills)
- [RawUGC request and response reference](reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details, JSON shapes, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAWUGC_API_KEY and may produce authenticated RawUGC API calls that create, edit, upload, delete, schedule, publish, or analyze media.]

## Skill Version(s):

0.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
