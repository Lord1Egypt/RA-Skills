## Description:

Audience Belief Mapper helps agents synthesize user-provided buyer interviews, win-loss notes, sales-call summaries, and support tickets into sourced belief maps, objection reframes, JTBD switching-force maps, and claim candidates marked for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, narrative, and go-to-market teams use this skill to turn user-provided customer evidence into a beachhead belief map, recurring objection reframes, and a JTBD four-forces switching map before authoring brand narrative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process customer interviews, sales notes, support tickets, and local memory files.

Mitigation: Use it only where saving those summaries to memory is acceptable, and avoid providing data the agent is not authorized to retain.

Risk: Proposed belief, reframe, or claim records could preserve unverified or misleading market language.

Mitigation: Review proposed claim and narrative records before allowing them to persist, and keep comparative claims marked [needs source] until approved.

## Reference(s):

- [Audience Belief Mapper on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/audience-belief-mapper)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured tables, sourced evidence labels, needs-source lists, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose memory records only after user confirmation; unverified quotes and comparative claims remain marked [needs source].]

## Skill Version(s):

19.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
