## Description:

Analyze the blast radius of upgrading, removing, or replacing a dependency by tracing imports, finding affected files, checking test coverage of impacted code, detecting breaking API changes, and generating safe upgrade plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before dependency upgrades, removals, or replacements to identify affected code, coverage gaps, reverse dependency impact, and migration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command snippets can turn package names or repository dependency versions into executable Python code.

Mitigation: Review and harden snippets before use, avoid untrusted repositories or crafted package names, pass dynamic values as arguments instead of interpolating them into Python source, avoid unpinned npx execution, and run audits without unnecessary secrets in the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/dependency-impact-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable text, JSON summaries, Markdown reports, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide CI-oriented exit-code guidance for low, high, or critical dependency impact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
