## Description:

Agent Error Logger helps agents record, retrieve, and analyze prior errors so they can recognize repeated failure patterns and suggest fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koonchaoso](https://clawhub.ai/user/koonchaoso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture task failures, search prior error records by keyword or tag, and surface reminders before similar work. It is useful for teams that want lightweight operational memory around recurring agent mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Error logs can persist raw task details, secrets, credentials, customer data, or untrusted third-party text.

Mitigation: Redact sensitive data before recording errors and avoid using this skill unchanged in sensitive projects without a log-retention and review process.

Risk: The artifact includes GitHub publishing guidance with a personal-access-token-in-URL command that could expose credentials.

Mitigation: Do not use PATs in repository URLs; use GitHub CLI authentication, credential helpers, or other token handling that avoids storing secrets in shell history or remotes.

Risk: The repository creation script can publish the current directory publicly.

Mitigation: Review the directory contents and intended visibility before running create-repo.sh or any publishing workflow.

## Reference(s):

- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [CoVE: Chain of Verification](https://arxiv.org/abs/2309.11495)
- [ClawHub skill page](https://clawhub.ai/koonchaoso/skills/agent-error-logger-new)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text, with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local error-log entries, search summaries, reminder checklists, and usage guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
