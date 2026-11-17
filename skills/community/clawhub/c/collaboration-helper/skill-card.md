## Description:

Track action items and coordination signals for the community, including quick task creation, status checks, and handoff notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

External users, developers, and community operators use this skill to log shared tasks, review current ownership and status, and record handoff notes during collaborative work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared task entries can persist owners, priorities, notes, and links in a local JSON file across runs.

Mitigation: Use the helper only for collaboration notes intended to be stored locally, and do not enter secrets, credentials, private customer data, or sensitive internal notes.

Risk: An alternate task data path can cause the helper to read or update a different JSON task file.

Mitigation: Point alternate data paths only at task files that the team intends this helper to inspect or modify.

## Reference(s):

- [Collaboration Helper reference](references/collaboration-guide.md)
- [Collaboration Helper ClawHub page](https://clawhub.ai/crimsondevil333333/skills/collaboration-helper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and JSON task structure guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates, reads, and updates local JSON task entries for shared collaboration state.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
