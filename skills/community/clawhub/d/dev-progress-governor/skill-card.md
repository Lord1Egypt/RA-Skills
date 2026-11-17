## Description:

Dev Progress Governor helps software development agents evaluate commit readiness, draft commit messages, append progress-log updates, summarize completed work, and track blockers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majmunu](https://clawhub.ai/user/majmunu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to keep AI-assisted implementation steps small, inspectable, and ready for disciplined commits. It supports commit-readiness checks, commit-message drafting, progress-log updates, blocker tracking, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested progress-log entries or commit messages may not match a project's preferred path or convention.

Mitigation: Review proposed log updates and commit messages before accepting them, and provide the desired log path or commit convention when it differs from the default.

Risk: Commit-readiness decisions may be incomplete when the agent only receives a diff or summary instead of the full project state.

Mitigation: Treat readiness decisions as based on the supplied evidence and provide missing context before committing when the scope is unclear.

## Reference(s):

- [Commit Guidelines](references/commit-guidelines.md)
- [Progress Log Template](references/progress-log-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with inline commit-message and progress-log blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commit-readiness status, changed-area summaries, suggested commit messages, progress-log entries, blockers, and a single next step.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
