## Description:

Code Debug Companion helps developers diagnose code errors, research similar solutions, generate fixes, and validate changes with tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage pasted stack traces, screenshots, or logs, research similar issues, generate code fixes and tests, and produce a concise debugging report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Error messages, screenshots, logs, or stack traces may contain secrets, proprietary code, or sensitive implementation details that could be exposed during external search.

Mitigation: Review and redact sensitive details before using web search or creating external issue-tracking records.

Risk: Generated fixes and tests may be incorrect, incomplete, or unsuitable for the target codebase.

Mitigation: Manually review proposed changes and run the relevant local tests before applying or committing them.

Risk: The workflow may write code or tests without clearly requiring user approval.

Mitigation: Require explicit human approval before modifying files, adding tests, or opening GitHub issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/code-debug-companion)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Structured Markdown debugging report with code and test-change summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnosis, related discussions, fix details, generated tests, and changed-file lists.]

## Skill Version(s):

1.0.0 (source: server release evidence and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
