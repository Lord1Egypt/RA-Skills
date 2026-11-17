## Description:

Helps agents create Baiyin AI singer training tasks, check task status, and return completed model results by taskId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit singer-model training requests to Baiyin with a public audio URL, monitor queued or processing tasks, and retrieve model IDs and demo links after success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a silent remote version check and self-update before handling user requests, which can modify installed instructions without explicit user approval.

Mitigation: Install or update through a trusted package manager with explicit approval and integrity verification, and remove or disable silent self-update behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuping520/skills/baiyin-cover-train-skill)
- [Baiyin API base URL](https://ai.hikoon.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown status summaries with JSON-shaped API payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include taskId, requestId, status, modelId, demoUrl, modelName, avatar, userTaskId, and trainType when available.]

## Skill Version(s):

1.0.3 (source: server release metadata and user changelog; artifact _meta.json lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
