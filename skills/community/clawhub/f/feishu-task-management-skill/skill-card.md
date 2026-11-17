## Description:

Manage Feishu tasks through a local Python toolkit that always has app credentials and can optionally act as a user for task APIs when OAuth user tokens are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owrig](https://clawhub.ai/user/owrig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, inspect, update, complete, reopen, delete, and manage members for Feishu tasks through a local command-line toolkit. It is most useful when task membership must be resolved from a synced local member directory and aliases rather than ad hoc contact lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships credential-bearing Feishu runtime configuration, including app secret and user token material.

Mitigation: Remove shipped credentials before release, rotate exposed Feishu secrets and tokens, and require each installation to configure its own credentials locally.

Risk: The release includes real member directory data used for local person resolution.

Mitigation: Remove real member data from the packaged artifact and document how users can sync their own directory with appropriate access controls.

Risk: Credential and member-cache handling may expose sensitive data on disk.

Mitigation: Store local secrets and member caches with owner-only file permissions and avoid committing generated runtime data.

Risk: OAuth callback and state handling is identified as unsafe by the security evidence.

Mitigation: Fix OAuth callback validation and state enforcement before normal installation or operational use.

Risk: API requests can be directed by configuration and should remain limited to official Feishu hosts.

Mitigation: Restrict allowed API destinations to official Feishu endpoints and validate configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/owrig/skills/feishu-task-management-skill)
- [API Alignment](references/api-alignment.md)
- [Member Sync Troubleshooting](references/member-sync-troubleshooting.md)
- [Permission Errors](references/permission-errors.md)
- [Task Edge Cases](references/task-edge-cases.md)
- [Feishu Open APIs base URL](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local toolkit commands that call Feishu APIs when credentials and permissions are configured.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
