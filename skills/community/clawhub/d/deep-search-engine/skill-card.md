## Description:

Searches Chinese and international sources for publication mentions, then checks candidate matches against titles, dates, and distinctive text to produce confidence-graded findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Communications, research, and editorial teams use the skill to check whether supplied content appeared online and to map likely reposts or mentions, with evidence for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search may send excerpts of unpublished or sensitive user text to third-party services.

Mitigation: Review privacy implications and avoid using unpublished or sensitive text unless its use with external search services is appropriate.

Risk: Weaknesses in result verification and link handling may produce unreliable publication matches or citations.

Mitigation: Check the linked source and confirm title, publication date, and distinctive body text before relying on a finding or citation.

Risk: Partial scan coverage can leave relevant sources unexamined, so missing results do not establish that content was never published.

Mitigation: Treat search coverage as incomplete, follow up through additional sources, and report unresolved items as pending rather than as confirmed absence.

## Reference(s):

- [Channel Matrix](references/channel-matrix.md)
- [Media Pool Reference](references/media-pool.md)
- [ClawHub release](https://clawhub.ai/haiyangchenbj/skills/deep-search-engine)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Confidence-graded findings JSON with verification notes, links, and pending items when evidence is incomplete.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings distinguish verified matches from lower-confidence or pending results.]

## Skill Version(s):

0.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
