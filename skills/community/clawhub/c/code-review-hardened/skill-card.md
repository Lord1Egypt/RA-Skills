## Description:

Provides comprehensive, security-focused code review guidance for React 19, Vue 3, Rust, TypeScript, Java, Python, C, and C++.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, assess architecture and security concerns, apply language-specific review checklists, and provide constructive review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows shell access for review validation, including builds and tests that may execute untrusted repository scripts.

Mitigation: Approve exact lint, test, and build commands before execution; inspect package scripts or build files first; prefer a disposable sandbox with no secrets and no network access.

Risk: Repository content, diffs, or review findings could be exposed if external analysis is requested through WebFetch or network-capable shell commands.

Mitigation: Use WebFetch only to retrieve documentation, never to send code or findings; do not pipe shell output to curl, wget, nc, scp, ssh, or similar tools.

Risk: Review workflows can cause unintended code changes or data loss if findings are auto-remediated or destructive commands are run during review.

Mitigation: Treat the skill as observational by default; require explicit user authorization for each specific fix and avoid destructive commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/code-review-hardened)
- [Publisher Profile](https://clawhub.ai/user/snazar-faberlens)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown review findings, summaries, checklists, and optional shell commands for local validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review output should use severity labels and avoid transmitting repository content or findings to external services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
