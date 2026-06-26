## Description: <br>
Evolver Plus helps an agent identify repeated errors, capability gaps, or inefficient workflows, propose self-improvements as Genes, and apply them under four safety levels with backups and approval gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangho](https://clawhub.ai/user/tsangho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage controlled self-improvement workflows for agents, including creating Gene proposals, assigning safety levels, backing up files, and routing higher-risk changes for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad automatic self-modification and rollback behavior that affects persistent memory, documentation, scripts, or agent behavior. <br>
Mitigation: Narrow allowed paths, require explicit approval for overwrites and behavior-changing edits, and review Gene proposals before execution. <br>
Risk: Unsupervised periodic review could create or apply unnecessary changes. <br>
Mitigation: Disable unsupervised periodic review unless it is needed, and keep PENDING, GENES, and AUDIT records for each change. <br>
Risk: Failed evolution or rollback can leave files in an unintended state. <br>
Mitigation: Verify backups before each change and test rollback paths before relying on automated recovery. <br>


## Reference(s): <br>
- [Gene Format](references/gene-format.md) <br>
- [Safety Levels](references/safety-levels.md) <br>
- [ClawHub Release Page](https://clawhub.ai/tsangho/evolver-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Gene records and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply file changes when permitted by its safety gates.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
