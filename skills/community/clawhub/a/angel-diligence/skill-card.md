## Description:

Pre-investment research and deal-memo generation for angel investors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

External investors use this skill to research private startups before an angel check, prepare for founder calls, and produce a cited diligence memo. It separates verified facts from company claims, labels unverifiable items, and avoids invest/pass recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs public web research about startups, which may expose confidential deck details if the agent uses private materials in search queries.

Mitigation: Use private deck notes only as local context, search with generic public terms, and never include deck numbers, customer names from the deck, or roadmap details in external queries.

Risk: A diligence memo can contain stale, unsupported, or misleading claims if sources are missing or dated poorly.

Mitigation: Require fetched citations for factual claims, date each cited fact, label unverifiable claims as could not verify, and manually review the memo before relying on it.

Risk: Readers may mistake the memo for investment advice.

Mitigation: Keep the output as evidence and a verdict scaffold only; do not emit an invest/pass recommendation or valuation anchor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/angel-diligence)
- [Skill instructions](SKILL.md)
- [Research prompt templates](patterns/research-prompts.md)
- [Illustrative memo example](examples/illustrative-memo.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diligence memo with inline citations and a sources list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local nine-section memo and presents the snapshot, verdict scaffold, and could-not-verify count for review.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
