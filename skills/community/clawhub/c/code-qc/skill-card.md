## Description:

Run a structured quality control audit on any codebase. Use when asked to QC, audit, review, or check code quality for a project. Supports Python, TypeScript, GDScript, and general projects. Produces a standardized report with PASS/WARN/FAIL verdict, covering tests, imports, type checking, static analysis, smoke tests, and documentation. Also use when asked to compare QC results over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isonaei](https://clawhub.ai/user/isonaei)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run structured quality control audits across Python, TypeScript, GDScript, and general codebases. It helps summarize tests, imports, type checking, static analysis, smoke tests, documentation, and baseline comparisons into human-readable QC results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audits can execute project code through test, import, build, and smoke-test steps.

Mitigation: Run the skill only on trusted repositories or inside a disposable, network-restricted environment with no secrets.

Risk: Tool installation and package-runner steps can invoke unpinned external tools.

Mitigation: Review proposed pip, npx, lint, and build commands before execution and pin tools where practical.

Risk: Auto-fix mode can mutate source files.

Mitigation: Require explicit review before enabling fix steps and inspect the resulting diff before accepting changes.

## Reference(s):

- [GDScript QC Profile](references/gdscript-profile.md)
- [General QC Profile](references/general-profile.md)
- [Python QC Profile](references/python-profile.md)
- [Ruff Rules Reference](references/ruff-rules.md)
- [TypeScript QC Profile](references/typescript-profile.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON baselines, summary text, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run project-specific checks, generated smoke tests, and optional auto-fix steps depending on user approval and environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
