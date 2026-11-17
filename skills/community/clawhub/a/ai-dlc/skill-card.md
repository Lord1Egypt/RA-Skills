## Description:

AI-DLC provides an adaptive AI-driven software development lifecycle for new projects, features, bug fixes, refactoring, migrations, and other development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydpz](https://clawhub.ai/user/sydpz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure software delivery from workspace discovery and requirements analysis through planning, design, code generation, and build/test work. It is suited to guided development workflows where users review and approve major phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User input may be recorded verbatim in aidlc-docs/audit.md, which can expose secrets, tokens, customer data, or regulated information.

Mitigation: Avoid entering sensitive data, add redaction or change the audit-log behavior before use, and keep audit.md out of source control when it may contain private information.

Risk: The workflow scans the workspace and can create or modify many aidlc-docs files, with application-code changes after approval.

Mitigation: Run it in a controlled workspace, review planned phases and generated files before approval, and inspect diffs before committing changes.

## Reference(s):

- [AI-DLC Skill Definition](artifact/SKILL.md)
- [Process Overview](artifact/references/common/process-overview.md)
- [Question Format Guide](artifact/references/common/question-format-guide.md)
- [Session Continuity](artifact/references/common/session-continuity.md)
- [Requirements Analysis](artifact/references/inception/requirements-analysis.md)
- [Workflow Planning](artifact/references/inception/workflow-planning.md)
- [Code Generation](artifact/references/construction/code-generation.md)
- [Build and Test](artifact/references/construction/build-and-test.md)
- [Security Baseline](artifact/references/extensions/security/baseline/security-baseline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, code changes, shell command blocks, configuration guidance, and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates AI-DLC workflow files under aidlc-docs and may guide application-code changes after user approval.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence, created 2026-03-30T17:26:44Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
