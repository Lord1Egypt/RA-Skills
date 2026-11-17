## Description:

Answers Arknights operator, investment, lore, terminology, and stage-strategy questions while using a local Doctor profile for personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morandot](https://clawhub.ai/user/morandot)

### License/Terms of Use:

MIT-0

## Use Case:

External Arknights players use this skill to get build priorities, skill and mastery advice, stage strategy, lore summaries, terminology explanations, and resource-planning guidance tailored to explicitly recorded local account facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions may execute a mutable remote shell script from the main branch.

Mitigation: Install from a pinned release or reviewed package, and inspect the install path before execution.

Risk: The skill creates and updates persistent local game-account profile data, including server, UID, roster, resources, goals, and preferences.

Mitigation: Use ARKNIGHTS_MEMORY_DIR deliberately, keep the profile on a trusted local machine, and delete the profile when retention is no longer wanted.

Risk: Version-sensitive Arknights guidance can become stale when live lookup is unavailable.

Mitigation: Require live lookup for current banners, events, and meta-sensitive advice, or clearly state that the answer is not based on current version data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/morandot/skills/arknights-skill)
- [Server-Resolved GitHub Source](https://github.com/morandot/arknights-skill/tree/main/arknights-skill)
- [Project Homepage](https://github.com/morandot/arknights-skill)
- [Quick Start](references/quickstart.md)
- [Answer Templates](references/answer-templates.md)
- [Doctor Profile Schema](references/doctor-profile-schema.md)
- [Style Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with occasional shell command and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local profile data when available; version-sensitive answers require live lookup or a freshness caveat.]

## Skill Version(s):

1.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
