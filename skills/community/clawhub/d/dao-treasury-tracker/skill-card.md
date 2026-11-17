## Description:

Tracks DAO and crypto protocol treasury composition with DeFiLlama treasury data, calculating own-token concentration, diversified-asset share, total treasury value, and a concentration risk label.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, researchers, and governance reviewers use this skill to evaluate whether a DAO treasury has diversified runway or is materially concentrated in its own governance token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the tool contacts DeFiLlama and reveals which protocol slugs are queried.

Mitigation: Run only when sharing queried protocol names with DeFiLlama is acceptable.

Risk: Treasury coverage depends on DeFiLlama; smaller, newer, or untracked DAOs may return no treasury data.

Mitigation: Treat skipped or missing results as coverage gaps and verify material decisions against additional sources.

Risk: The output is a current balance-sheet snapshot and does not estimate runway, spending rate, or future token price movement.

Mitigation: Use the concentration label as a screening signal, not as a complete financial risk assessment.

## Reference(s):

- [DeFiLlama Treasury API](https://api.llama.fi/treasury/{slug})
- [DeFiLlama Protocols API](https://api.llama.fi/protocols)
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/skills/dao-treasury-tracker)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples, plus table or JSON treasury analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries DeFiLlama for user-provided protocol slugs and reports lookup errors per slug.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
