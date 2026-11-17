## Description:

Cron expression explainer that translates standard five-field cron syntax into human-readable English or French and can validate expressions locally without an LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and operators use this skill to understand cron expressions they did not write, document scheduled jobs, and perform a lightweight pre-deployment validation check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports standard five-field cron expressions and does not support Quartz syntax, seconds fields, or next-occurrence calculation.

Mitigation: Use it for explanation and lightweight validation only; use scheduler-native checks or a cron library such as croniter for runtime scheduling and advanced cron dialects.

Risk: The security guidance says not to treat its validation as the sole production safety gate until edge-case parsing bugs and stale documentation are fixed.

Mitigation: Review the expression against the target scheduler and test it in the deployment environment before enabling production jobs.

Risk: Localized documentation may imply broader language coverage than the implementation provides.

Mitigation: Expect only English and French explanations from the current implementation and review localized documentation before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-cron-whisperer)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON, with optional Markdown code blocks for CLI and Python usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local output for standard five-field cron expressions; explanations are limited to English and French.]

## Skill Version(s):

0.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
