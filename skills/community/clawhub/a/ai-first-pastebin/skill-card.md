## Description:

Use 呵.tw as an AI-first pastebin to shorten URLs, store shareable non-secret agent handoff notes, recover tagged pastes, and reduce LLM token usage across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joustonhuang](https://clawhub.ai/user/joustonhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to shorten long URLs and store or retrieve shareable, non-secret handoff content through the hosted 呵.tw service when full content would consume unnecessary context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential, regulated, or secret content could be sent to the hosted 呵.tw service.

Mitigation: Upload only user-approved shareable content; do not send secrets, credentials, private logs, regulated personal data, or content that should remain local.

Risk: The hosted service may rate limit requests or be temporarily unavailable.

Mitigation: Honor Retry-After responses, back off on 429 responses, and avoid relying on the service for content that must stay available locally.

## Reference(s):

- [呵.tw agent-facing documentation](https://呵.tw/llms.txt)
- [ClawHub skill page](https://clawhub.ai/joustonhuang/skills/ai-first-pastebin)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Networked CLI calls return JSON; the QR command returns a URL.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
