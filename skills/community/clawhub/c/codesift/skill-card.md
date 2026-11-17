## Description:

Review code for systemic defects, broken contracts, redundant or unused code, ineffective validation gates, and unsupported performance claims; present evidence-backed findings and wait for approval before editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanw1](https://clawhub.ai/user/zanw1)

### License/Terms of Use:

MIT

## Use Case:

Developers use CodeSift to investigate code changes, code health issues, and large or mixed-language repositories. It presents evidence-backed findings and a remediation plan before making approved edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project test and benchmark commands may write files or perform other project-defined actions.

Mitigation: Review commands before running them and use a disposable checkout for tests or benchmarks that may write files.

Risk: Registry checks read package-manager settings and disclose dependency names.

Mitigation: Use the documented offline mode when registry access or dependency-name disclosure is unsuitable.

Risk: Optional evaluation scaffolds can overwrite files in their target directory.

Mitigation: Run evaluation scaffolds only in an empty directory.

Risk: A static security assessment does not verify runtime behavior.

Mitigation: Run relevant checks where appropriate and report the scope and limits of the evidence.

## Reference(s):

- [CodeSift on ClawHub](https://clawhub.ai/zanw1/skills/codesift)
- [Review patterns and evidence guidance](references/patterns.md)
- [Polyglot repository guidance](references/polyglot.md)
- [Python guidance](references/python.md)
- [C guidance](references/c.md)
- [C++ guidance](references/cpp.md)
- [Rust guidance](references/rust.md)
- [JavaScript and TypeScript guidance](references/javascript.md)
- [Database systems guidance](references/database-systems.md)
- [Example review report](references/report-example.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown findings and remediation plan; code changes and validation commands for approved items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings distinguish reproduced, confirmed_static, and hypothesis evidence; scope and unreviewed areas are reported.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
