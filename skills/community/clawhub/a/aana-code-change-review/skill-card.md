## Description:

Reviews and verifies code changes for scope, correctness, security, testing, secrets, and risks before commits, PRs, or deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code-editing agents use this skill to keep code changes scoped, reviewable, honestly tested, secret-free, and reversible before commits, pull requests, releases, or deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional checker payloads could expose secrets, private records, full logs, full diffs, or unrelated repository files if sent without redaction.

Mitigation: Use redacted summaries only, and send payloads only through a user- or administrator-approved checker or manual review path.

Risk: High-risk code changes, destructive commands, commits, pull requests, publishing, or deployments may need explicit approval or human review.

Mitigation: Require approval before destructive actions and defer security-sensitive, migration, deploy, release, or broad refactor changes to a verified review path.

## Reference(s):

- [AANA Code Change Review Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-code-change-review)
- [Skill Instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Review Payload Schema](artifact/schemas/code-change-review.schema.json)
- [Redacted Review Payload Example](artifact/examples/redacted-code-change-review.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with an optional redacted JSON review payload shape]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; it does not execute commands, install dependencies, persist memory, or write files on its own.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
