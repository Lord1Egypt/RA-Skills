## Description:

Orchestrates cross-platform enterprise IM workflows across Feishu, DingTalk, and WeCom CLIs for reporting, task synchronization, notifications, marketing distribution, and meeting coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and business automation teams use this skill to plan and execute Feishu, DingTalk, and WeCom CLI workflows for reports, task sync, broadcasts, marketing distribution, and meeting coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running third-party CLIs can introduce package provenance and authentication risks.

Mitigation: Install only the required CLIs, verify package provenance, prefer pinned or project-local installs, and authenticate with minimal platform scopes.

Risk: Generated commands may post, create, update, or delete enterprise content on behalf of the authenticated user.

Mitigation: Review commands before execution, use preview or dry-run modes when available, and require explicit confirmation for destructive actions.

Risk: Cross-platform broadcasts can amplify mistakes or send sensitive content to the wrong audience.

Mitigation: Check recipients and message content before sending, limit broadcast rate, and report any platform failure instead of silently retrying.

## Reference(s):

- [Lark CLI](https://github.com/larksuite/cli)
- [DingTalk Workspace CLI](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [WeCom CLI](https://github.com/WecomTeam/wecom-cli)
- [ClawHub skill page](https://clawhub.ai/lm203688/skills/china-im-workflow-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific command sequences and pre-execution checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
