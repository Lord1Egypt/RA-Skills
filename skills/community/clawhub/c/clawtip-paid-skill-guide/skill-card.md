## Description:

Guides developers through creating ClawTip paid skills with local order creation, SM4 encryption, and local payment testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liulian822](https://clawhub.ai/user/liulian822)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this guide to structure ClawTip paid skills, create encrypted local order files, and test payment-driven service generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment verification guidance could lead users to accept invalid or mismatched payments.

Mitigation: Verify payment credentials through the trusted ClawTip component before generating paid services, fail closed on merchant or recipient errors, and use test or sandbox accounts where possible.

Risk: Local order files can expose payment workflow data if handled carelessly.

Mitigation: Protect local order files and review the generated paid-skill workflow before installing or following it.

## Reference(s):

- [ClawTip Official Developer Guide](https://clawtip.jd.com/guide)
- [ClawHub Skill Page](https://clawhub.ai/liulian822/skills/clawtip-paid-skill-guide)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment workflow guidance and local order-file handling instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
