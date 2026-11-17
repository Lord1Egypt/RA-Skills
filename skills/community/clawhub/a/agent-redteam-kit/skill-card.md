## Description:

Helps developers screen English and Chinese prompts for common jailbreak and dangerous-request patterns, then report risk levels and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to triage prompts and agent inputs before launch, review detected jailbreak or dangerous-request patterns, and decide what to harden or block.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local pattern scan is not a complete security assessment and can miss attacks.

Mitigation: Use it for preliminary triage and conduct broader adversarial testing before deployment.

Risk: Broad security terms may trigger scanning during ordinary discussion, and flagged results need interpretation.

Mitigation: Invoke the scan deliberately on a chosen prompt or file and review any block or review result before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-redteam-kit)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Text or Markdown risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports matched patterns and risk tiers with a review or block disposition; local scanner also returns status codes.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
