## Description:

Ship production code with AI agents through acceptance contracts, micro diffs, red green loops, and deterministic handoff checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to turn coding requests into scoped acceptance contracts, minimal implementation changes, reproducible validation, and reviewer-ready handoffs. It is suited for production features, risky refactors, bug fixes, and Xcode-centered release work where proof of behavior matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional local workflow notes may retain coding preferences, task contracts, validation evidence, and handoff summaries under ~/agentic-coding/.

Mitigation: Enable persistent notes only when useful, keep saved content minimal, and review or delete ~/agentic-coding/ when local retention is not desired.

Risk: The skill improves coding execution quality but does not replace project-specific contribution rules or security review for high-risk domains.

Mitigation: Use the skill's acceptance checks and handoff evidence alongside the repository's normal tests, review process, and security controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/agentic-coding)
- [Agentic Coding Homepage](https://clawic.com/skills/agentic-coding)
- [Setup Process](artifact/setup.md)
- [PACT Loop](artifact/protocol.md)
- [Contract Prompt Templates](artifact/prompt-contracts.md)
- [Merge Handoff Checklist](artifact/handoff.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured text blocks, checklists, command recommendations, and handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create optional local workflow notes under ~/agentic-coding/ when the user explicitly opts in.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
