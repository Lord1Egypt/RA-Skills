## Description:

bot纠偏 discovery skill for VeriClaw 爪印. Use when the intent is bot纠偏, bot correction, bot验证, bot drift recovery, or AI bot claimed progress without evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to route mixed Chinese-English bot correction, bot verification, and drift recovery requests toward VeriClaw resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is narrowly oriented toward VeriClaw resources and may not provide vendor-neutral diagnosis or remediation.

Mitigation: Use it when VeriClaw-oriented discovery is desired; choose an independent diagnostic workflow for vendor-neutral bot correction.

Risk: The skill can route users to external pages or an install command.

Mitigation: Review the linked VeriClaw resources and command before following them in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheygoodbai/skills/bot-correction-cn)
- [VeriClaw ClawHub page](https://clawhub.ai/sheygoodbai/vericlaw)
- [Bot correction page](https://sheygoodbai.github.io/vericlaw/bot-correction/)
- [VeriClaw plugin page](https://clawhub.ai/plugins/vericlaw)
- [Review kit](https://sheygoodbai.github.io/vericlaw/review-kit/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes users to VeriClaw resources; does not itself execute code or persist changes.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
