## Description:

Complete one-time Feishu browser authorization and cache a local user_access_token so later feishu-bitable-sync runs can write Bitable rows as the current user instead of app identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to complete a one-time Feishu OAuth flow, cache user-level credentials locally, and enable later Bitable synchronization to run under the current user's identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Feishu user access and refresh tokens on the local machine.

Mitigation: Keep the cache path private, restrict local access to ~/.codex/feishu-auth/content-system-sync.json, and delete the cache or revoke the Feishu app authorization when it is no longer needed.

Risk: The generated authorization report may include user identity metadata such as name, open_id, issue time, and expiry time.

Mitigation: Avoid sharing the generated auth report when Feishu identity metadata is sensitive.

Risk: The OAuth flow depends on a Feishu app configuration and the local callback http://127.0.0.1:14578/callback.

Mitigation: Confirm the Feishu app has web application capability enabled and that the callback URL is configured before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/feishu-user-auth)
- [Publisher profile](https://clawhub.ai/user/abigale-cyber)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown authorization report plus local token cache metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an auth result report under content-production/published and stores Feishu user token cache data locally.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
