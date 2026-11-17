## Description:

Audit an upstream agent skill, SKILL.md, skill repository, or lifecycle workflow before adapting it for ClawHub, Codex, Claude Code, or a public Skool skill sprint, with a PORT, REWRITE, or REJECT decision and no global install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to review upstream agent skills before adapting or publishing them. It produces a portability decision, rewrite plan, safety findings, proof checklist, and install or publish gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewers may provide private skill sources, credentials, account-only material, or local-only details as audit input.

Mitigation: Use redacted or public-safe source material and replace sensitive details with placeholders before drafting public artifacts.

Risk: The skill can influence whether another skill is installed or published, so incorrect recommendations could affect an active project.

Mitigation: Require static review, duplicate-name checks, public-surface redaction checks, a dry run, and explicit user approval before any non-local install.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PORT, REWRITE, or REJECT verdict with concise review findings and next actions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
