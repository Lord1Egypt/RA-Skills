## Description:

Self-learning system for crypto trading that logs trades with indicators and market context, analyzes win/loss patterns, generates trading rules, and can update agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totaleasy](https://clawhub.ai/user/totaleasy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to keep a local crypto trade journal, analyze historical results, generate data-driven trading rules, and optionally update an agent MEMORY.md file with those rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade history is stored locally in plaintext.

Mitigation: Avoid logging sensitive account details, restrict local file access, and review data/trades.json before sharing or publishing the workspace.

Risk: Generated trading rules can be written into an agent memory file and influence later trading decisions.

Mitigation: Use the dry-run mode first and manually review the proposed MEMORY.md changes before applying them.

Risk: Rules generated from limited trade history may produce misleading trading guidance.

Mitigation: Require an adequate sample size, treat generated rules as review inputs, and avoid using them as automatic trade execution instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/totaleasy/skills/crypto-self-learning)
- [ClawHub Publisher Profile](https://clawhub.ai/user/totaleasy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown guidance with JSON files for logged trades and generated rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local data/trades.json and may append learned rules to a specified MEMORY.md file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
