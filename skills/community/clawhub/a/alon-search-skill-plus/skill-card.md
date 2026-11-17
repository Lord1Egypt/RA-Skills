## Description:

Search agent skills across trusted directories, ClawHub, and GitHub adaptation candidates with explicit ranking and safety filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alondotsh](https://clawhub.ai/user/alondotsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill users use this skill to find existing agent skills before building one from scratch, with ranked results and safety notes across trusted directories, ClawHub, and GitHub adaptation candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses unpinned remote code.

Mitigation: Review the installer path before installing, prefer a pinned package version and repository commit, and avoid running the installer with elevated privileges.

Risk: Runtime searches can send queries to external sources and may surface lower-trust results.

Mitigation: Review results manually, especially ClawHub, aggregators, and GitHub adaptation candidates, before installing or recommending them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alondotsh/skills/alon-search-skill-plus)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown ranked shortlist with source labels, relevance notes, safety notes, and adaptation sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search keywords, GitHub stars, recency, installation hints, and lower-trust source review notes when relevant]

## Skill Version(s):

0.1.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
