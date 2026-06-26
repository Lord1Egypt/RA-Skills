## Description: <br>
Self-learning system for crypto trading that logs trades with full context, analyzes win and loss patterns, and auto-updates trading rules to support continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totaleasy](https://clawhub.ai/user/totaleasy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to maintain a local crypto trade journal, analyze win and loss patterns, generate data-driven trading rules, and update agent memory with reviewed lessons from prior trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading rules may be misleading if based on sparse or biased trade history. <br>
Mitigation: Review generated rules before relying on them and treat them as journal-derived guidance, not financial advice. <br>
Risk: The memory update script can modify a user-selected MEMORY.md file. <br>
Mitigation: Use --dry-run first and keep backups before applying learned rules to memory. <br>


## Reference(s): <br>
- [Crypto Self-Learning ClawHub Release](https://clawhub.ai/totaleasy/crypto-self-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON trade and rule files, and Markdown memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and jq; writes local trade history and can update a user-selected MEMORY.md file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
