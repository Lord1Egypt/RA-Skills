## Description:

COC 7th Edition tabletop assistant. Dice rolling (success levels, bonus/penalty dice, critical/fumble), SAN system (X/Y loss expressions, temporary/indefinite insanity, INT check memory suppression), investigator management, madness tables / occupations / weapons / NPCs, combat initiative, configurable rules system (critical/fumble ranges, SAN thresholds, preset strict/lenient variants). Supports --seed for reproducible rolls, --json for programmatic chaining, and investigator state persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangtianjiao](https://clawhub.ai/user/jiangtianjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External tabletop players and Keepers use this skill to run Call of Cthulhu 7th Edition sessions from an agent. It supports COC-specific dice checks, sanity resolution, investigator state, table lookups, and combat or chase ordering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted dice or SAN expressions may cause unreliable or excessive local processing because dice-count limits are not documented as enforced.

Mitigation: Use the skill with trusted tabletop inputs and review dice or SAN expressions before execution.

Risk: Investigator data and rules are stored in local session.json, and delete or reset actions are immediate.

Mitigation: Back up session.json before destructive session-management commands and confirm the intended investigator or rules target.

## Reference(s):

- [Coc Helper ClawHub Skill Page](https://clawhub.ai/jiangtianjiao/skills/coc-helper)
- [jiangtianjiao ClawHub Publisher Profile](https://clawhub.ai/user/jiangtianjiao)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Human-readable CLI text, or JSON when --json is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18; writes local session.json state for investigators and rules.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and SKILL.md v1.0 note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
