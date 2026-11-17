## Description:

BugPack - AI-powered bug tracking and fixing toolkit. List bugs, view bug details with screenshots, and fix bugs automatically. Includes three workflows: list-bugs, view-bug, fix-bug. Requires BugPack server running locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duhuazhu](https://clawhub.ai/user/duhuazhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use BugPack to list tracked bugs, inspect bug context with screenshots and related files, apply fixes, and update bug status through a local BugPack server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm server package.

Mitigation: Pin bugpack-mcp to a reviewed version before use.

Risk: The skill can lead an agent to edit code and update bug status without explicit safety gates.

Mitigation: Review proposed code diffs before permitting the agent to PATCH bug status or update descriptions.

## Reference(s):

- [BugPack ClawHub Skill Page](https://clawhub.ai/duhuazhu/skills/bugpack)
- [BugPack Publisher Profile](https://clawhub.ai/user/duhuazhu)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce code edits and bug status updates based on BugPack server responses.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
