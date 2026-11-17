## Description:

Helps agents create Baiyin AI digital-human video tasks, check task status, and retrieve final video results for lip-sync and body-driven digital-human models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuping520](https://clawhub.ai/user/jiuping520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Baiyin digital-human video workflows through an agent: select a live model, create a task with audio and first-frame image inputs, query progress, and return final video links when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a silent remote self-update before normal use, so reviewed instructions could be replaced without user awareness.

Mitigation: Use only after update handling is removed or moved to an explicit trusted package-management flow; review and scan the installed skill before deployment.

Risk: Digital-human task creation may send images, voice/audio, private URLs, and prompts to Baiyin services.

Mitigation: Upload or submit only content that is approved for sharing with Baiyin, and avoid sensitive, proprietary, or private personal data unless authorized.

Risk: Authenticated API calls require BAIYIN_API_KEY.

Mitigation: Store the API key in a managed secret or environment variable, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected.

## Reference(s):

- [Baiyin Open Platform API base](https://ai.hikoon.com)
- [ClawHub skill page](https://clawhub.ai/jiuping520/skills/baiyin-digital-human-lipsync)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Concise Markdown or plain text with task IDs, task status, model choices, upload guidance, and final result links when returned by the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIYIN_API_KEY and public or uploaded URLs for required audio and first-frame image inputs.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
