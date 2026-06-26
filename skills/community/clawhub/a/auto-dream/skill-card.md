## Description: <br>
Auto Dream consolidates long-running agent memory through a four-phase Orient, Gather, Merge, and Prune workflow that preserves durable facts while removing stale or sensitive context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Auto Dream to keep agent memory accurate, concise, and useful before handoff, after daily reflection, or when context has become stale, duplicated, contradictory, or too large. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit and prune stored memory, which may remove useful long-term context if applied too aggressively. <br>
Mitigation: Review the summary after it runs and ask for a preview before pruning important long-term context. <br>
Risk: Incorrect consolidation can preserve stale, duplicated, or contradictory memory as durable facts. <br>
Mitigation: Use the reported open questions and contradiction count to review uncertain changes before relying on the consolidated memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brasco05/auto-dream) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/brasco05) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Short Markdown status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update existing memory files before returning a concise consolidation summary.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
