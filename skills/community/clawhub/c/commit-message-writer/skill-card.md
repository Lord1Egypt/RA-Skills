## Description:

Generate Conventional Commit messages, PR titles, and summaries from git diffs, code snippets, or change descriptions for any project or language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnguyen1996](https://clawhub.ai/user/lnguyen1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn git diffs, code snippets, or plain change descriptions into commit messages, PR titles, and short PR summaries. It supports projects that want consistent commit wording across Conventional Commits, Angular, GitHub squash-merge, or plain descriptive styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted diffs, snippets, or descriptions may contain sensitive code, credentials, or private issue details.

Mitigation: Review and redact sensitive information before sharing change context with an agent.

Risk: Suggested commit messages may misclassify the change type, scope, or breaking-change status.

Mitigation: Review the generated message against the actual diff and project release conventions before committing.

Risk: The skill asks the agent to remember lightweight usage categories over time.

Mitigation: Avoid relying on that behavior for private analytics and limit retained context to non-sensitive categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnguyen1996/skills/commit-message-writer)
- [ClawHub publisher profile](https://clawhub.ai/user/lnguyen1996)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with commit message, PR title, and PR summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May vary by requested convention, scope, and breaking-change status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
