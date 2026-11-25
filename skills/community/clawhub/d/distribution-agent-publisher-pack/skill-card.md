## Description:

Turn 1–9 images into platform-specific captions and mood-matched music hints, then route to mock, dry-run, or real publishers with publish logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milab-bit](https://clawhub.ai/user/milab-bit)

### License/Terms of Use:


## Use Case:

External creators, social media operators, and developers use this skill to prepare platform-specific social publishing packs from small image sets, including captions, hashtags, music-search hints, and publish result logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare payloads for real public posting and cross-posting.

Mitigation: Keep publishing in mock or dry-run mode until account scopes, platform choices, privacy settings, and cross-posting behavior are reviewed.

Risk: Generated captions, hashtags, and platform options may be posted publicly if real publishing is enabled.

Mitigation: Require explicit user approval before any public publish and review generated payloads for accuracy, policy compliance, and intended audience.

Risk: Publisher integrations may require platform tokens or account credentials.

Mitigation: Store credentials in environment variables or a local secrets mechanism and avoid committing tokens to the repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milab-bit/skills/distribution-agent-publisher-pack)
- [PROMPTS.md](artifact/PROMPTS.md)
- [TEMPLATES.md](artifact/TEMPLATES.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [Strict JSON publish packs and publish log JSON, with generated captions, hashtags, platform options, and music search hints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses 1–9 image filenames or URLs, a theme, target platforms, language, optional style, and optional mood hint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
