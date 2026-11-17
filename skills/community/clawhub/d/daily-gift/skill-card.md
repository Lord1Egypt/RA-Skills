## Description:

Generate personalized, relationship-aware daily gifts in H5, image, video, text, or interactive text-play formats to mark meaningful moments and milestones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiawei248](https://clawhub.ai/user/jiawei248)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to decide whether an onboarding moment, scheduled daily run, milestone, anniversary, or manual creative prompt deserves a personalized gift, then produce the gift in the format that best fits the moment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and summarize personal conversations, store taste and emotional context, and save positively shared images.

Mitigation: Review data retention expectations and storage paths before installation, and enable recurring runs only when this personal-context handling is acceptable.

Risk: Optional third-party providers, hosted previews, remote asset fetching, video support, and Freesound may expose user data or credentials.

Mitigation: Keep those optional network features disabled until endpoint allowlists, integrity checks, and clearer privacy controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiawei248/skills/daily-gift)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Setup flow](artifact/references/setup-flow.md)
- [Daily run flow](artifact/references/daily-run-flow.md)
- [Manual run flow](artifact/references/manual-run-flow.md)
- [Delivery policy](artifact/references/delivery-policy.md)
- [Asset manifest](artifact/references/asset-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, generated text, HTML/H5 artifacts, image or video generation prompts, JSON state updates, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workspace state, gift history, taste-profile records, H5 files, image or video assets, and optional hosted previews.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-04-27T13:22:15Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
