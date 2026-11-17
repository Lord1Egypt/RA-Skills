## Description:

CodeByteLens helps agents inspect Python code by listing symbols, searching definitions, and producing simple complexity and call-analysis output from local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect local Python projects, find symbols or definitions, and generate lightweight code-structure and complexity reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation overstates pyright and tree-sitter integration compared with the bundled local AST and ripgrep helper behavior.

Mitigation: Treat results as lightweight local code-inspection guidance and verify findings with project tests, type checkers, or code review before acting.

Risk: The setup guidance uses an unpinned dependency install for pyright.

Mitigation: Install dependencies in a virtual environment and pin versions before using the skill in repeatable or commercial workflows.

Risk: Definition search and call-analysis behavior may be incomplete or broken.

Mitigation: Use the output as a starting point for investigation and confirm symbol locations or call relationships with source inspection.

## Reference(s):

- [CodeByteLens ClawHub release](https://clawhub.ai/lxr-666/skills/codebytelens)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command output; analyzes local Python files only.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
