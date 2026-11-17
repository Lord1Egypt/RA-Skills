## Description:

Launch and manage Cursor Cloud Agents via the official API v0 for delegated coding tasks, automatic PR creation, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siaslfs](https://clawhub.ai/user/siaslfs)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to launch Cursor Cloud Agents against authorized repositories, monitor their progress, send follow-up instructions, and collect PR or status results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Cursor API key and can start a detached watcher that continues using that key after the visible command returns.

Mitigation: Use the minimum required repository access, avoid passing the key with --api-key, prefer a tightly permissioned key file or secure credential store, and rotate or revoke keys when access is no longer needed.

Risk: Feishu notifications can expose task status or conversation excerpts for sensitive work.

Mitigation: Leave Feishu notifications disabled for sensitive repositories or prompts, and avoid setting CURSOR_NOTIFY_TARGET or --notify unless the destination is approved.

Risk: Creating agents can make repository changes, create PRs, and incur Cursor API usage costs.

Mitigation: Confirm the repository, branch, task prompt, and PR intent before launch; keep pre-flight checks enabled; review generated PRs before merge.

## Reference(s):

- [Cursor Cloud Agent API documentation](https://cursor.com/docs/cloud-agent/api/endpoints)
- [How to Get Your Cursor Cloud Agent API Key](references/get-token.md)
- [Cursor dashboard](https://cursor.com/dashboard)
- [ClawHub skill page](https://clawhub.ai/siaslfs/skills/cursor-cloud-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and API-derived status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cursor agent IDs, branch names, PR URLs, final status, and truncated conversation summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
