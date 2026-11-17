## Description:

Catalyst Design helps agents produce catalyst composition, structure, synthesis, condition-optimization, and validation guidance from a layered, traceable methodology and optional catalyst-search literature matrices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andypeng09](https://clawhub.ai/user/andypeng09)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use this skill to turn a catalyst design goal into a Markdown design proposal covering material choices, synthesis strategy, operating conditions, traceability, and experimental validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional methodology self-updates can persistently change the skill's own reference files.

Mitigation: Keep the methodology read-only during normal use; enable updates only after reviewing the proposed entries, source tags, confidence labels, and active or pending status.

Risk: Catalyst design guidance can be incorrect or under-evidenced if empirical entries are treated as confirmed literature.

Mitigation: Require each recommendation to show its source tag and confidence, and use catalyst-search re-checks for directions supported only by empirical evidence.

## Reference(s):

- [Catalyst Design Methodology System](artifact/references/design_methodology.md)
- [Traceability Registry](artifact/references/methodology_registry.md)
- [Methodology Update Protocol](artifact/references/methodology_update_protocol.md)
- [Design Proposal Template](artifact/templates/design_proposal.md)
- [ClawHub Skill Page](https://clawhub.ai/andypeng09/skills/catalyst-design-skill)
- [Project Homepage](https://github.com/ANDYPENG09/catalyst-design-skill)
- [Companion Catalyst Search Skill](https://github.com/ANDYPENG09/catalyst-search-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown design proposal with traceability tables and citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advice labels methodology source tags, confidence, literature support, empirical guesses, and validation steps.]

## Skill Version(s):

1.0.5 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
