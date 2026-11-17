## Description:

Generates short AI videos from text prompts through the Chilltion API and helps agents manage Chilltion sessions, streaming status, credits, costs, and account balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragondean](https://clawhub.ai/user/dragondean)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create Chilltion video-generation sessions from concise text prompts, monitor progress, retrieve video or chat URLs, and review account credit usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Chilltion API calls could be redirected if CHILLTION_BASE_URL is changed.

Mitigation: Keep CHILLTION_BASE_URL set to https://chilltion.com for normal use and use only isolated development credentials when testing any alternate endpoint.

Risk: Prompts and messages sent through the skill leave the local machine and may consume account credits.

Mitigation: Avoid sending sensitive content, confirm user intent before generation, and check balance or session cost when credit use matters.

Risk: Untrusted prompts, wrappers, or automation could steer script arguments or account-level API operations.

Mitigation: Do not allow untrusted input to set environment variables or script arguments, and limit calls to the user-authorized Chilltion task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragondean/skills/generate-free-ai-video-via-chilltion)
- [Chilltion service](https://chilltion.com)
- [Publisher profile](https://clawhub.ai/user/dragondean)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHILLTION_API_KEY; responses can include session IDs, SSE progress events, credit data, chat URLs, and video URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-05-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
