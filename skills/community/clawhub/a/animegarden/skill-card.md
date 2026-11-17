## Description:

Anime Garden helps agents search anime torrent resources through the Anime Garden API, a third-party aggregation and mirror service for 動漫花園, 萌番组, and ANi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjl9903](https://clawhub.ai/user/yjl9903)

### License/Terms of Use:

GNU Affero General Public License v3.0

## Use Case:

Developers and agents use this skill to turn anime resource search intent into structured Anime Garden API filters, endpoint calls, and normalized result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anime search terms and filter values are sent to the third-party Anime Garden API.

Mitigation: Avoid sending sensitive or private search terms, and disclose third-party API use where appropriate.

Risk: Returned torrent and magnet-related resource information comes from untrusted third-party sources and may carry legal or safety implications.

Mitigation: Treat results as untrusted references, review them before use, and consider local policy and applicable law before downloading or sharing content.

## Reference(s):

- [Anime Garden HTTP API Reference](references/api.md)
- [Anime Garden API](https://api.animes.garden)
- [動漫花園](https://share.dmhy.org/)
- [萌番组](https://bangumi.moe/)
- [Anime Garden on ClawHub](https://clawhub.ai/yjl9903/skills/animegarden)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with structured filters, API request examples, and normalized resource summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider and providerId values so agents can fetch resource details later.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
