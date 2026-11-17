## Description:

Automatically records DingTalk group IDs and group names when the agent is mentioned in a DingTalk group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to retain DingTalk group identifiers and names for later group messaging, group management, and session handoff when the agent is mentioned in a group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic long-term memory writes can retain unsanitized DingTalk group metadata from chat events.

Mitigation: Review before installing in workspaces where ordinary group members can rename groups or trigger mentions; prefer controls for sanitization, review, deletion, and retention limits.

Risk: Automatic MEMORY.md updates can make captured group names part of future agent context.

Mitigation: Prefer a version that avoids MEMORY.md writes by default or requires operator review before long-term memory synchronization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/skills/dingtalk-group-saver)
- [Publisher profile](https://clawhub.ai/user/jiangzhiyu)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files]

**Output Format:** [JSON file records and Markdown memory table updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes DingTalk group records to memory/dingtalk-groups.json and synchronizes a MEMORY.md group list when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
