## Description:

A Chinese-language agent self-review skill that helps agents identify memory-recall failures, missing workflow steps, edit-anchor mistakes, and inefficient debugging paths, then use mistake archives, root-cause classification, and verification loops to correct them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mowenqwq](https://clawhub.ai/user/mowenqwq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to improve agents that maintain local notes or memory. It provides a Chinese-language checklist and taxonomy for reviewing repeated agent mistakes, updating mistake archives, and verifying corrections before acting again.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may treat local mistake archives as unquestionable truth or let stale notes override current task evidence.

Mitigation: Use archives as aids to verification, compare them with current evidence, and resolve conflicts explicitly before acting.

Risk: Mistake archives and memory notes may contain sensitive operational details if users add them during real work.

Mitigation: Keep archives under user control, avoid storing secrets or unnecessary personal data, and review notes before sharing them.

Risk: Process guidance can still be incorrect or misleading for a specific deployment even when it contains no executable code.

Mitigation: Review the markdown guidance before deployment and adapt checklist items to the local workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mowenqwq/skills/agent-mistake-patterns)
- [ClawHub publisher profile](https://clawhub.ai/user/mowenqwq)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown guidance with checklists and short command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language content; no executable code]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
