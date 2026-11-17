## Description:

Concept Radar finds, deduplicates, and evaluates evidence-backed concepts from one URL or a pool of authors, then exports the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and knowledge workers use the skill to track a field or examine an author's ideas, turning selected source material into evidence-backed concept cards. It supports one-off URL scans and recurring reviews of a configured author pool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags possible GitHub token exposure through unvalidated URLs or redirects; its review was partial.

Mitigation: Treat the release as review-needed, review the missing scan paths, and avoid making a GitHub token available until the token-handling concern is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/concept-radar)
- [Evidence policy](artifact/references/evidence-policy.md)
- [Quality rubric](artifact/references/quality-rubric.md)
- [State contract](artifact/references/state-contract.md)
- [Card schema](artifact/references/card-schema.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Evidence-backed concept cards and scan summaries in Markdown and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cards include maturity, evidence confidence, bounded next-step recommendations, and source links.]

## Skill Version(s):

0.1.4 (source: SKILL.md frontmatter; server-resolved release metadata confirms version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
