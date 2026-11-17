## Description:

Fix a BugPack issue by reading its context, locating relevant code, applying a fix, and updating the local BugPack status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duhuazhu](https://clawhub.ai/user/duhuazhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when asked to resolve a BugPack issue. It guides them through fetching bug context, reviewing screenshots and related files, applying code changes, and updating the BugPack status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may mark a BugPack issue as fixed before the code change has been adequately validated.

Mitigation: Review the code diff and confirm tests or manual checks support the fix before relying on the final status update.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duhuazhu/skills/bugpack-fix-bug)
- [Publisher Profile](https://clawhub.ai/user/duhuazhu)

## Skill Output:

**Output Type(s):** [Code, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline code blocks and concise status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local BugPack API requests and code diff summaries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
