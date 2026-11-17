## Description:

Helps agents draft and review influencer partnership agreements, covering scope, compensation, usage rights, exclusivity, FTC disclosure, clause red flags, and negotiation points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, legal-operations, and creator-partnership teams use this skill after a partnership is agreed in principle to draft influencer agreements, review incoming agency terms, and prepare negotiation guidance. It is intended for general contract support and template drafting, with legal counsel review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle confidential contract terms and directs agents to persist drafted agreements, review memos, and signed deal terms in shared memory.

Mitigation: Use it only in hosts that block unapproved persistent writes or require explicit user approval before saving confidential contract material.

Risk: The security evidence flags a mismatch between read-oriented capability metadata and artifact behavior that describes memory writes.

Mitigation: Review write behavior before installation and limit deployment to environments where proposed writes can be inspected or disabled.

Risk: Generated contract drafts and clause guidance may be incomplete for a specific jurisdiction, industry, or deal structure.

Mitigation: Require qualified legal review before executing any agreement produced or reviewed with this skill.

## Reference(s):

- [Contract Helper Templates and Reference Packs](artifact/references/templates.md)
- [Contract Helper Skill Page](https://clawhub.ai/aaron-he-zhu/skills/contract-helper)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown agreement drafts, review memos, clause explanations, red-flag checklists, and negotiation tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes influencer contract parameters, drafted clauses, review findings, and negotiation ranges.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
