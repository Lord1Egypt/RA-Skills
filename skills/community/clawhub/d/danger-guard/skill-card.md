## Description:

Danger Guard helps agents intercept potentially destructive commands, require verification, and provide alerting and configuration guidance before risky operations proceed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to add guardrails around destructive filesystem, Git, Docker, SQL, privilege, and remote-script operations across supported agent tooling. It is intended to reduce accidental or unauthorized damage from commands issued through an AI assistant or connected chat workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to enter an OS sudo, admin, or login password into an AI chat and stores an unsalted SHA256 verifier.

Mitigation: Do not enter real OS passwords into chat; prefer native OS authorization or scoped, revocable verification mechanisms.

Risk: The skill can persistently rewrite agent instruction files and add global shell aliases or wrappers that intercept common terminal commands.

Mitigation: Review all proposed file changes before installation, keep protections project-local when possible, and avoid the shell wrapper unless persistent command interception is acceptable.

Risk: Security review classified the release as suspicious despite its defensive intent.

Mitigation: Review before installing and scan the artifact in the target environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomaszhou22/skills/danger-guard)
- [Publisher profile](https://clawhub.ai/user/thomaszhou22)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent agent instructions, shell aliases, git hooks, and alerting configuration.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
