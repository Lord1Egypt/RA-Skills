## Description:

Enterprise-grade code review agent that reviews PRs, diffs, or code files for security vulnerabilities, performance issues, error handling gaps, architecture smells, and test coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review GitHub pull requests, local diffs, pasted code, or source files for security, performance, error handling, architecture, and reliability issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PR comments or review recommendations could be posted to repositories as external write actions.

Mitigation: Review generated comments and confirm repository permissions before allowing the agent to post to pull requests.

Risk: Heartbeat or cron-style review prompts could repeatedly inspect or comment on repositories if targets and schedules are unclear.

Mitigation: Use scheduled workflows only after confirming the target repositories, schedule, and posting permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review reports with severity ratings, SPEAR scores, findings, suggested fixes, and prioritized recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub PR review comments and local git or GitHub CLI commands when the user asks for repository-based review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
