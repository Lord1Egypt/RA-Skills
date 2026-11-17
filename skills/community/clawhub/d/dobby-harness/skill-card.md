## Description:

Provides multi-agent orchestration with task decomposition, parallel execution, result aggregation, and self-improving workflows for complex coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panb-kg](https://clawhub.ai/user/panb-kg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multiple coding agents for complex software tasks such as code review, test generation, documentation, CI/CD configuration, and stateful workflow improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad agent or session data to local plaintext WAL, buffer, or log files.

Mitigation: Avoid storing secrets, tokens, full environment dumps, private code context, or personal data unless restrictive file permissions, redaction, retention limits, and encryption are added.

Risk: CI/CD and PR-commenting examples can affect external review or deployment surfaces when connected to real integrations.

Mitigation: Require explicit user approval and safe target environments before enabling automated comments, commits, deployment configuration, or CI/CD actions.

Risk: Broad automation guidance may produce changes that are inappropriate for sensitive workspaces.

Mitigation: Review generated code, configuration, and workflow outputs before applying them, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panb-kg/skills/dobby-harness)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [HARNESS-ARCHITECTURE.md](artifact/HARNESS-ARCHITECTURE.md)
- [WORKFLOWS.md](artifact/WORKFLOWS.md)
- [SELF-IMPROVEMENT.md](artifact/SELF-IMPROVEMENT.md)
- [SECURITY-AUDIT.md](artifact/SECURITY-AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, JSON-style reports, generated code or configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow reports, test or documentation drafts, CI/CD configuration drafts, and local state artifacts when the persistence features are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
