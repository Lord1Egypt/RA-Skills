## Description:

Provides a seven-step debugging workflow and offline Python tools for log triage, secret-redacted environment snapshots, and reproduction report checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use the skill to reproduce software bugs, narrow down likely causes, verify fixes, and document regression evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some described debugging features may not be implemented in the supplied files.

Mitigation: Check which commands and features are present in the release before relying on them for a debugging workflow.

Risk: Broad activation triggers may bring the skill into unrelated conversations.

Mitigation: Confirm that the request concerns software debugging and check that the response addresses the reported issue.

Risk: The security scan is partial because some referenced paths were missing.

Mitigation: Review the available package files and verify the relevant behavior before relying on it.

## Reference(s):

- [debug-pro on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/debug-pro-zh)
- [Publisher profile: zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, JSON]

**Output Format:** [Markdown with shell commands and structured triage output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Markdown triage card and JSON facts when using the bundled tools.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
