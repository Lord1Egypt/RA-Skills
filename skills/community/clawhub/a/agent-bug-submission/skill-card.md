## Description:

Submits defect information to TeamCycle, tracks defect lifecycle status, and records entries in Feishu Bitable and Feishu Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiciferyi](https://clawhub.ai/user/luiciferyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and internal teams use this skill to collect defect details, submit TeamCycle bug reports, track defect status, and record report metadata in Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose a TeamCycle password through chat history, shell history, process listings, or copied command examples.

Mitigation: Replace password-based command-line authentication with a protected credential flow before use, and avoid entering real passwords into chat or command-line examples.

Risk: The skill depends on a referenced bug-reporter implementation that was not included in the release evidence.

Mitigation: Review and verify the bug-reporter implementation and its TeamCycle API behavior before installing or executing the skill.

Risk: Defect records may be written to Feishu or TeamCycle destinations that are not appropriate for the user's data.

Mitigation: Use the skill only in a controlled internal environment after confirming the intended Feishu and TeamCycle destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luiciferyi/skills/agent-bug-submission)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured defect fields, command examples, and defect tracking details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce TeamCycle defect links, defect IDs, and local defect records when the required integrations are available.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
