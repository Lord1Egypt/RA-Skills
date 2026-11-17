## Description:

Helps people plan short decluttering sessions by tracking household items, estimating container needs, prioritizing easy high-volume removals, and preparing disposal manifests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Individuals and household helpers use this skill to inventory clutter, estimate bags and boxes, plan manageable room-by-room sessions, and organize items for sale, donation, recycling, or disposal. It is not a substitute for clinical support for hoarding disorder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local household-item details and decisions are stored in a JSON file that can be overwritten at the selected path.

Mitigation: Run in a dedicated folder, choose --db paths deliberately, and protect or back up the registry as needed.

Risk: Container, storage-cost, and resale estimates may not match actual space or local prices.

Mitigation: Treat estimates as planning aids and check dimensions, market prices, and donation values before acting.

## Reference(s):

- [Declutter Pilot on ClawHub](https://clawhub.ai/voronindenis5/skills/declutter-pilot)
- [Decision Science of Decluttering](references/decision-science.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Plain text or Markdown guidance and a local JSON item registry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session plans, progress summaries, container estimates, and disposition manifests; numeric estimates are approximate.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
