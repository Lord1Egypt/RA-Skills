## Description: <br>
Complete one-time Feishu browser authorization and cache a local `user_access_token` so later `feishu-bitable-sync` runs can write Bitable rows as the current user instead of app identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abigale-cyber](https://clawhub.ai/user/abigale-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to complete a one-time Feishu browser OAuth flow and cache a user token before running Bitable syncs as the current user. It is intended for first-time authorization, expired-token refresh, or workflows that need user identity instead of tenant identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill caches a Feishu user token locally, and that cache should be treated as sensitive credential material. <br>
Mitigation: Protect ~/.codex/feishu-auth/content-system-sync.json like a password, avoid syncing it to backups or shared folders, and delete or revoke the token when it is no longer needed. <br>
Risk: The OAuth flow authorizes a Feishu app to act with the permissions granted by the user. <br>
Mitigation: Install only if the Feishu app and runtime helper are trusted, and review the Feishu app permissions before authorizing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abigale-cyber/feishu-user-auth) <br>
- [Publisher profile](https://clawhub.ai/user/abigale-cyber) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown authorization report plus a local JSON token cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an authorization result report under content-production/published and caches Feishu token data under ~/.codex/feishu-auth/content-system-sync.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
