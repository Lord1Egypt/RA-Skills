## Description:

Interact with the AIOZ Stream API to manage videos, audio, playlists, players, webhooks, analytics, payments, chapters, and transcripts on the AIOZ decentralized streaming platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinhbui3004](https://clawhub.ai/user/vinhbui3004)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to guide authenticated AIOZ Stream workflows, including media upload, transcoding, playlist and player management, webhooks, analytics, payments, chapters, and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AIOZ Stream account secrets and can guide actions with account-level impact.

Mitigation: Install only when comfortable granting agent access to the AIOZ Stream account; prefer a least-privileged only_upload key with a short TTL and rotate keys after use.

Risk: The skill includes destructive or sensitive workflows such as uploads, deletes, webhook changes, and API key creation or deletion.

Mitigation: Require explicit confirmation before uploads, deletes, webhook changes, or API key creation and deletion.

## Reference(s):

- [AIOZ Stream API base URL](https://api.aiozstream.network/api)
- [AIOZ Stream Skill on ClawHub](https://clawhub.ai/vinhbui3004/skills/aioz-stream-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for AIOZ Stream public and secret keys before API actions and uses structured status templates for uploads, webhooks, and media operations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
