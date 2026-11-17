## Description:

Review Apollo ecosystem issues with a classify-first workflow and draft maintainer-grade replies that directly answer user asks, clarify support boundaries, and provide actionable next paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nobodyiam](https://clawhub.ai/user/nobodyiam)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to review Apollo ecosystem GitHub issues, separate behavior reports from consultative support questions, validate the relevant evidence path, and draft concise maintainer responses. It is especially suited for issue triage that needs reproducibility checks, support-boundary statements, and publish confirmation before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting a drafted maintainer reply can publish incorrect repository, issue, or comment content if the target and body are not reviewed.

Mitigation: Use draft-only mode by default and require explicit final review of the repository, issue number, and exact comment body before posting.

Risk: Raw placeholder posting commands can mishandle untrusted reply text or expose behavior tied to GitHub credentials.

Mitigation: Use scoped GitHub credentials and structured GitHub API submission, such as serializer-produced JSON or `gh api --input`, before enabling posting.

## Reference(s):

- [Diagnostic Playbook](references/diagnostic-playbook.md)
- [Reply Templates](references/reply-templates.md)
- [Apollo Issue Review on ClawHub](https://clawhub.ai/nobodyiam/skills/apollo-issue-review)
- [Publisher Profile](https://clawhub.ai/user/nobodyiam)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline shell commands and optional YAML handoff block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only by default; posting to GitHub requires explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
