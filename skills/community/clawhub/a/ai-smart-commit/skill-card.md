## Description:

Smart Commit helps agents analyze code diffs or change descriptions to draft Conventional Commits messages, PR or MR descriptions, release notes, and change-impact assessments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caingao](https://clawhub.ai/user/caingao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn repository diffs, commit history, or change descriptions into clear commit messages, PR descriptions, release notes, and risk-aware change summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs and git history may include private code or secrets.

Mitigation: Use explicit prompts, review the text before sharing, and avoid exposing sensitive diffs to untrusted systems.

Risk: Generated commit, PR, or release-note text may misstate the intent, scope, or risk of a change.

Mitigation: Review generated output against the actual diff and project conventions before committing or publishing it.

## Reference(s):

- [Smart Commit on ClawHub](https://clawhub.ai/caingao/skills/ai-smart-commit)
- [OpenClaw](https://openclaw.ai)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt language to the repository or user request and may include multiple commit-message options in quick mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
