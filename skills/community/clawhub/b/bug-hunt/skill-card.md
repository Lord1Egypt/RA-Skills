## Description:

Use when asked to find bugs, hunt for correctness issues, sweep a codebase for defects, or verify a repo behaves as intended. Not for style or architecture review; this is defect-finding only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to sweep a codebase for correctness defects and verify candidate findings before reporting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plausible but incorrect bug candidates could mislead maintainers.

Mitigation: Require an adversarial verification pass and a concrete triggering scenario before reporting a finding.

Risk: Reproduction tests may affect the reviewed repository or its environment.

Mitigation: Run reproduction tests only when safe and keep them sandboxed.

Risk: Optional companion skills and the referenced lint script are outside the reviewed bundle.

Mitigation: Review and scan those components separately before relying on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/solomonneas/skills/bug-hunt)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown code-review report with a verdict, scorecard, verified findings, and backlog]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review; findings require adversarial verification and concrete triggers.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
