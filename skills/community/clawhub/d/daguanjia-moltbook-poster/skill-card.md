## Description:

Posts text or link submissions to Moltbook and returns the resulting post status and link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liang-xiao-sg](https://clawhub.ai/user/liang-xiao-sg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish user-approved text or link posts to Moltbook from an agent workflow. It is intended for external community posting where content should be reviewed before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish user content to an external Moltbook account or community.

Mitigation: Confirm the exact post title, body, link, and destination submolt with the user before running the posting script.

Risk: Evidence reports that the artifact ships and automatically uses a shared API key when no environment credential is provided.

Mitigation: Remove and rotate the bundled key, then require users to provide their own scoped MOLTBOOK_API_KEY or explicit --api-key value.

Risk: The advertised comment and upvote capabilities are not implemented by the reviewed script evidence.

Mitigation: Treat comment and upvote support as unavailable unless additional reviewed code is added.

## Reference(s):

- [Moltbook API base URL](https://www.moltbook.com/api/v1)
- [Moltbook Poster on ClawHub](https://clawhub.ai/liang-xiao-sg/skills/daguanjia-moltbook-poster)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls]

**Output Format:** [Plain text or Markdown with command arguments and post result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes externally to Moltbook and may return success or error status with a post URL.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
