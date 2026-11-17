## Description:

On-demand German public-media documentary picks filtered against a personal profile, delivered via the configured output channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arturites](https://clawhub.ai/user/arturites)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to curate German public-media documentary recommendations from a downloaded Mediathek catalog, ranked against a local personal profile and delivered through their configured output channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and caches a public media catalog before producing recommendations.

Mitigation: Install only in environments where cached public catalog data is acceptable, and apply resource limits for shared or low-resource systems.

Risk: Recommendations can include external media-library links from the catalog.

Mitigation: Treat recommendation links as external links and prefer URL validation before use in shared or sensitive environments.

Risk: The skill reads or creates PROFILE.md and sends recommendations through the configured output channel.

Mitigation: Use only with an output channel the user has configured and secured, and avoid including raw profile content in delivered recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arturites/skills/dokutipp)
- [Publisher profile](https://clawhub.ai/user/arturites)
- [Project homepage](https://github.com/arturites/DokuTipp)
- [Mediathek catalog download](https://liste.mediathekview.de/Filmliste-akt.xz)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown recommendations in German with optional media-library links, backed by JSON candidate data from the curation script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects four recommendations and writes skill-generated files under the skill data directory.]

## Skill Version(s):

1.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
