## Description:

AI-DLC is an adaptive, AI-guided software development workflow for planning, requirements, design, code generation, build, and test tasks with human approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydpz](https://clawhub.ai/user/sydpz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide greenfield or brownfield software work through workspace detection, requirements analysis, workflow planning, design, code generation, and build/test review. It is intended for new projects, features, bug fixes, refactoring, migrations, and other development tasks that benefit from structured approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow records user input verbatim in aidlc-docs/audit.md, which can capture secrets, credentials, private keys, tokens, personal data, or confidential snippets.

Mitigation: Do not provide sensitive information during use unless the audit behavior is changed or you explicitly accept that it may be stored; prefer redaction, explicit opt-in, and an ignored or deletable audit log.

Risk: The workflow broadly inspects project files and creates repository files.

Mitigation: Install and run it only in workspaces where broad project inspection and file creation are acceptable, and review generated changes before committing or deploying them.

## Reference(s):

- [Aidlc ClawHub skill page](https://clawhub.ai/sydpz/skills/aidlc)
- [sydpz publisher profile](https://clawhub.ai/user/sydpz)
- [AI-DLC skill definition](artifact/SKILL.md)
- [Process overview](artifact/references/common/process-overview.md)
- [Requirements analysis](artifact/references/inception/requirements-analysis.md)
- [Workflow planning](artifact/references/inception/workflow-planning.md)
- [Code generation](artifact/references/construction/code-generation.md)
- [Build and test](artifact/references/construction/build-and-test.md)
- [Baseline security rules](artifact/references/extensions/security/baseline/security-baseline.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, generated documentation files, code edits, configuration changes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update aidlc-docs workflow files and project files in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
