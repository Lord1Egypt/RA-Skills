## Description:

Guides evidence-driven adversarial reviews and root-cause repairs of code, designs, APIs, infrastructure, tests, and agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aakashh242](https://clawhub.ai/user/aakashh242)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Gauntlet to investigate suspected defects, substantiate findings, and, when authorized, repair root causes and verify the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from an untrusted or changing source may expose the agent to altered instructions.

Mitigation: Install from a pinned, trusted source, especially for user-wide installation.

Risk: Review notes in the optional local ledger may contain sensitive code, secrets, or production details.

Mitigation: Keep the ledger in a private directory outside version control and review notes before recording sensitive material.

Risk: Applying deep-review or repair guidance to routine edits may waste effort or change code unexpectedly.

Mitigation: Reserve the skill for deep reviews and authorize repairs explicitly.

## Reference(s):

- [ClawHub release](https://clawhub.ai/aakashh242/skills/gauntlet)
- [Server-resolved source repository](https://github.com/aakashH242/gauntlet)
- [Review protocol](SKILL.md)
- [Review triage](references/triage.md)
- [Evaluation guide](evals/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown review report with findings, evidence, checks, and optional code repairs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only by default; optional private SQLite tracking ledger.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
